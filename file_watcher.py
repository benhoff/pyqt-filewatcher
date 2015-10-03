import sys
from PyQt5 import QtCore


class DirWatcher(object):
    def __init__(self):
        self.file_watcher = QtCore.QFileSystemWatcher()

        self.directory_changed = self.file_watcher.directoryChanged
        self.file_changed = self.file_watcher.fileChanged

    def add_paths(self, paths):
        if not isinstance(paths, list):
            self.file_watcher.addPath(paths)
        else:
            self.file_watcher.addPaths(paths)


class AutoLoadInterface(object):
    def __init__(self, interface):
        self.plugin_pair = []
        self.interface = interface 
        self.notifier = None

    def add_autoappend_plugin(self, klass, list_reference):
        self.plugin_pair.append((klass, list_reference))

    def directory_changed(self, directory_path=None):
        # TODO: Make sure no state is saved with this method call
        locations = self.interface.get_plugin_locations(directory_path)
        if not locations:
            return
        loaded_modules = self.interface.load_modules(locations)
        if not loaded_modules:
            # TODO: unload modules
            return
        plugins = self.interface.get_plugins_from_modules(loaded_modules)
        if not plugins:
            # TODO: unload modules
            return

        autoload_plugins = []
        loaded_modules = []
        for plugin in plugins:
            for klass, list_ref in self.plugin_pair:
                if isinstance(plugin, klass):
                    list_ref.append(plugin)
                    autoload_plugins.append(plugin)
                    # TODO: add to loaded modules
                    break

        unused_modules = []
        for plugin in plugins:
            # TODO: add logic to check if in `loaded_modules`
            if plugin not in autoload_plugins:
                # TODO: unload module?
                pass

        self.interface.add_plugins(autoload_plugins)

    #FIXME: i don't believe this is correct
    def _unload_modules(self, modules):
        for module in modules:
            del sy.modules[module]
