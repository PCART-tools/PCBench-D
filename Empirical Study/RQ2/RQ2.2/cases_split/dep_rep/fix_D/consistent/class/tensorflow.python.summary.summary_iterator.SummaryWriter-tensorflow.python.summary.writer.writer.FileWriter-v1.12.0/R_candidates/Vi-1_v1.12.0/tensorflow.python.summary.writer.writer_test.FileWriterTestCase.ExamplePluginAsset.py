    class ExamplePluginAsset(plugin_asset.PluginAsset):
      plugin_name = "example"

      def assets(self):
        return {"foo.txt": "foo!", "bar.txt": "bar!"}
