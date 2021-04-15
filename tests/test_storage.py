import tempfile
import pytest

from pgbackup import storage

@pytest.fixture
def infile():
    file = tempfile.TemporaryFile('r+b')
    file.write(b"Testing")
    file.seek(0)
    return file

def test_storing_file_locally(infile):
    """
    Writes content from one file-like to another
    """
    outfile = tempfile.NamedTemporaryFile(delete=False)
    storage.local(infile, outfile)
    with open(outfile.name, 'rb') as file:
        assert file.read() == b"Testing"

def test_storing_file_on_s3(mocker, infile):
    """
    Writes content from one readable to S3
    """
    client = mocker.Mock()

    storage.s3(client, infile, "bucket", "file-name")

    client.upload_fileobj.assert_called_with(infile, "bucket", "file-name")

