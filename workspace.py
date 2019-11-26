import os



class Workspace:

    def __init__(self, pathname):
        self.pathname = pathname
        self.ignore = [".git", "__pycache__" ]

    def list_files(self, dir=None):
        if dir is None:
            dir = self.pathname
        if os.path.isdir(dir):
            allfiles =  os.listdir(dir)

            filenames =  [x for x in allfiles if x not in self.ignore]
            paths = []
            for file_path in filenames:
                path = os.path.join(dir, file_path)
                paths = paths + self.list_files(path)
            return  paths

        else:
            return [os.path.relpath(dir, self.pathname)]

    def stat_file(self, path):
        stat = os.stat( os.path.join(self.pathname, path)  )
        return stat

    def read_file(self, path):
        f = open(path, "rb")
        return f.read()
    
    def list_dir(self, dirname=None):
        path = None
        if dirname is None:
            path = self.pathname
        else:
            path = os.path.join(self.pathname, dirname)
        allfiles =  os.listdir(path)

        filenames =  [x for x in allfiles if x not in self.ignore]
        stats = {} 


        for name  in filenames:
            relative = os.path.relpath( os.path.join(path, name), self.pathname )
            stats[relative] = os.stat(os.path.join(path, name)) 


        return stats


    def apply_migration(self, migration):
        self.apply_change_list(migration, "delete")
        for dir in sorted(migration.rmdirs, reverse=True):
            self.remove_directory(dir)

        for dir in sorted(migration.mkdirs):
            self.make_directory(dir)


        self.apply_change_list(migration, "update")
        self.apply_change_list(migration, "create")

    def remove_directory(self, dirname):
        try:
            os.rmdir(os.path.join(self.pathname, dirname))
        except (OSError, FileNotFoundError) as error:    
            pass

    def make_directory(self, dirname):
        path = os.path.join(self.pathname, dirname)
        stat = self.stat_file(dirname)

        if stat is not None:
            if stat_m.S_ISREG(stat.st_mode):
                os.remove(path)

            if stat_m.S_ISDIR(stat.st_mode):
                try:
                    os.mkdir(path)
                except OSError as exc:
                    pass







    def apply_change_list(self, migration, action):
        import pdb; pdb.set_trace()
        for filename, entry  in migration.changes[action]:
            path = os.path.join(self.pathname, filename)
            os.remove(path)
            if action == "delete":
                continue

            data = migration.blob_data(entry.oid)

            file = open(path , "wb+")
            file.write(data)
            file.close()
            
            
