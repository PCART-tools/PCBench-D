def unroll(uf, IndexType, InType, OutType, use_weights, isa, fused, use_offsets):
    def compute(regid, InType, use_weights, isa, prefetch):
        code = []

        if InType == "float":
            code.append(
                "        vop%d = _mm256_fmadd_ps(vwgt, _mm256_loadu_ps(ip + (%d)), vop%d);"  # noqa
                % (regid, regid, regid)
            )
        elif InType == "at::Half":
            code.append(
                "        vop%d = _mm256_fmadd_ps(\n"
                "            vwgt,\n"
                "            _mm256_cvtph_ps(\n"
                "                _mm_loadu_si128(reinterpret_cast<const __m128i*>(ip + (%d)))),\n"  # noqa
                "            vop%d);" % (regid, regid, regid)
            )
        elif InType == "uint8_t":
            code.append(
                "        vop%d = _mm256_fmadd_ps(\n"
                "            vwgt,\n"
                "            _mm256_cvtepi32_ps(_mm256_cvtepu8_epi32(\n"
                "                _mm_loadl_epi64(reinterpret_cast<const __m128i*>(ip + (%d))))),\n"  # noqa
                "            _mm256_add_ps(vop%d, vbio));" % (regid, regid, regid)
            )
        else:
            assert False

        if prefetch:
            code.append(
                "        _mm_prefetch(\n"
                "            reinterpret_cast<const char*>(&ip_next_T0[%d]), _MM_HINT_T0);"
                % (regid)
            )
        else:
            code.append(
                "        // skip unnecessary prefetch of (&ip_next_T0[%d])" % (regid)
            )

        return code

    code = []
    code.append("    // unrolling " + str(uf) + " times")

    if use_offsets:
        code.append(
            "    for ("
            + IndexType
            + " rangeIndex = 0; rangeIndex < output_size; ++rangeIndex) {"
        )
    else:
        code.append(
            "    for ("
            + IndexType
            + " rangeIndex = 0; rangeIndex < output_size; ++rangeIndex) {"
        )

    code.append("      " + OutType + "* op = &out[rangeIndex * block_size];")
    for i in range(0, uf):
        j = 8 * i
        code.append("      __m256 vop" + str(j) + " = _mm256_setzero_ps();")

    # inner loop
    if use_offsets:
        code.append(
            "      if (dataInd != offsets[rangeIndex] - offsets[0]) {\n"
            + "        return false;\n"
            + "      }"
        )
        code.append("""\
      int64_t end_offset = offsets[rangeIndex + 1];
      int64_t length = end_offset - offsets[rangeIndex];""")
        code.append(
            "      for ("
            + "int64_t"
            + " start = dataInd; dataInd < end_offset - offsets[0];\n           ++dataInd) {"  # noqa
        )
    else:
        code.append(
            "      if (dataInd + lengths[rangeIndex] > index_size) {\n"
            + "        return false;\n"
            + "      }"
        )
        code.append(
            "      for ("
            + IndexType
            + " start = dataInd; dataInd < start + lengths[rangeIndex];\n           ++dataInd) {"  # noqa
        )
    code.append("        const " + IndexType + " idx = indices[dataInd];")
    code.append(
        "        if (idx < 0 || idx >= data_size) {\n"
        + "          return false;\n"
        + "        }"
    )

    if InType == "uint8_t":
        code.append("        " + OutType + " wgt = 1.f;")
        code.append("        " + OutType + " bio;")
        code.append("        if (weights) {")
        code.append(
            "          wgt = weights[IS_WEIGHT_POSITIONAL ? (dataInd - start) : dataInd];"  # noqa
        )
        code.append("        }")
        if fused:
            code.append(
                "        const float* scale_bias = reinterpret_cast<const float*>(\n"
                "            &input[idx * fused_block_size + block_size]);"
            )
            code.append("        bio = wgt * scale_bias[1];")
            code.append("        wgt = wgt * scale_bias[0];")
        else:
            code.append("        bio = wgt * scale_bias[2 * idx + 1];")
            code.append("        wgt = wgt * scale_bias[2 * idx];")
        code.append("        __m256 vbio = _mm256_set1_ps(bio);")
    else:
        code.append("        " + OutType + " wgt = 1.f;")
        code.append("        if (weights) {")
        code.append(
            "          wgt = weights[IS_WEIGHT_POSITIONAL ? (dataInd - start) : dataInd];"  # noqa
        )
        code.append("        }")
    code.append("        __m256 vwgt = _mm256_set1_ps(wgt);")

    code.append("        const {}* ip = &input[idx * fused_block_size];".format(InType))
    code.append(
        "        const {} next_T0 = (dataInd < index_size - prefdist_T0)\n"
        "            ? (dataInd + prefdist_T0)\n            : dataInd;".format(
            IndexType
        )
    )
    code.append("        const " + IndexType + " idx_pref_T0 = indices[next_T0];")
    code.append(
        "        if (idx_pref_T0 < 0 || idx_pref_T0 >= data_size) {\n"
        + "          return false;\n"
        + "        }"
    )

    code.append(
        "        const {}* ip_next_T0 = "
        "&input[idx_pref_T0 * fused_block_size];".format(InType)
    )

    for i in range(0, uf):
        j = 8 * i
        cachelinesize = 64
        byteoffset = sizeof[InType] * j
        prefetch = (byteoffset % cachelinesize) == 0
        code.extend(compute(j, InType, use_weights, isa, prefetch))
    code.append("      }")

    if use_offsets:
        code.append("      if (!normalize_by_lengths || length == 0) {")
    else:
        code.append("      if (!normalize_by_lengths || lengths[rangeIndex] == 0) {")
    for i in range(0, uf):
        j = 8 * i
        code.append("        _mm256_storeu_ps(&op[" + str(j) + "], vop" + str(j) + ");")
    code.append("      } else {")
    # inv of length
    if use_offsets:
        code.append("        __m256 vlen_inv = _mm256_set1_ps(1.0f / length);")
    else:
        code.append("        __m256 vlen_inv = _mm256_set1_ps(1.0f / lengths[rangeIndex]);")
    for i in range(0, uf):
        j = 8 * i
        code.append(
            "        _mm256_storeu_ps(&op["
            + str(j)
            + "], _mm256_mul_ps("
            + "vop"
            + str(j)
            + ", vlen_inv));"
        )
    code.append("      }")

    code.append("    }")
    return code
