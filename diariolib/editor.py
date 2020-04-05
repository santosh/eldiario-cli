import datetime
import logging
import os
import pathlib
import subprocess
import tempfile

logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.expanduser("~")+"/eldiario.log",
    format="%(asctime)s:%(levelname)s %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %Z",
)

class Editor:
    message = None
    def __init__(self):
        pass

    def get_text_from_new(self):
        """Get text from the newly created or editor from db."""

        ctime, path = self.new_editor()

        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))

        logging.info("file modification time: {}".format(mtime))

        logging.debug("ctime: %s" % ctime)
        logging.debug("mtime: %s" % mtime)

        if mtime > ctime:
            logging.info("Feels like we should proceed.")
            with open(path) as entry_content:
                fd = entry_content.read()
                self.message = fd
        else:
            logging.info("No new content were generated.")

        return self.message


    @staticmethod
    def preferred_editor():
        """Checks if $EDITOR is set. If not, look up for vim executable.
        If that's false. Use vi"""
        
        defined_editor = os.getenv("EDITOR", False)
        if defined_editor:
            return defined_editor
        elif os.path.exists('/usr/bin/vim') or os.path.exists('/bin/vim'):
            return 'vim'
        else:
            return 'vi'

    def new_editor(self):
        """Creates a temporary file, opens preferred editor. 

        Returns:
            file_creation_time: temp file creation time
            tempfile_path: path to the created file"""

        # FIXME: Use datetime string for tempfile filename
        _, tempfile_path = tempfile.mkstemp(suffix=".md", prefix="eldiario_", text=1)

        epoch_ctime = os.path.getctime(tempfile_path)
        file_creation_time = datetime.datetime.fromtimestamp(epoch_ctime)
        
        editor = subprocess.Popen([Editor.preferred_editor(), tempfile_path])
        editor.wait()
        
        logging.info("file creation time: {}".format(file_creation_time))
        
        return file_creation_time, tempfile_path

    def editor_from_message(self, ctime, text):
        """Returns an Editor representing mongo row."""

        _, tempfile_path = tempfile.mkstemp(suffix=".md", prefix="eldiario_", text=1)        

        with open(tempfile_path, "w") as writeto:
            writeto.write(text)

        editor = subprocess.Popen([Editor.preferred_editor(), tempfile_path])
        editor.wait()

        with open(tempfile_path) as readfrom:
            return readfrom.read()


def clean_editor_cache():
    for f in pathlib.Path("/tmp").glob("eldiario_*"):
        os.unlink(f)


if __name__ == "__main__":
    Editor.new_editor()
