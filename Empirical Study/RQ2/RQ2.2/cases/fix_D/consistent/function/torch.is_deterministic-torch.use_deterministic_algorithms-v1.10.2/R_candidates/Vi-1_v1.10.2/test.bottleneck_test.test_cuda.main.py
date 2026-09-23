def main():
    data = torch.randn(10, 50).cuda()
    model = Model().cuda()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.0001)
    for i in range(10):
        optimizer.zero_grad()
        loss = model(data)
        loss.backward()
        optimizer.step()
