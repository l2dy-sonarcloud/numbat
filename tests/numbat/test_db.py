from numbat import SourcetrailDB
from numbat.base import NameHierarchy, NameElement, NodeType

import pathlib
import shutil
import pytest
import os

TMP_PATH = 'generated'

@pytest.fixture(scope='session', autouse=True)
def prepare_and_clean():
    """
        This function will be called once before running all 
        the test and once after all the test have been run.
    """
    
    # Create a new directory
    os.makedirs(TMP_PATH)
    yield
    # Delete it 
    shutil.rmtree(TMP_PATH)

@pytest.fixture()
def test_create_db():
    print('test_create_db')
    path = '%s/db.srctrldb' % TMP_PATH

    # Clean if already exists 
    if os.path.exists(path):
        os.remove(path)

    # Create a new database
    srctrl = SourcetrailDB()
    try:
        srctrl.create(path)
        srctrl.close()
        assert True
    except Exception as e:
        print(e)
        assert False

def test_open_database(test_create_db):
    print('test_create_symbol')
    path = '%s/db.srctrldb' % TMP_PATH

    # Open an existing database
    srctrl = SourcetrailDB()
    try:
        srctrl.open(path)
        srctrl.clear()
        srctrl.close()
        assert True
    except Exception as e:
        print(e)
        assert False

def test_record_file(test_create_db):
    path = '%s/db.srctrldb' % TMP_PATH

    # Open an existing database
    srctrl = SourcetrailDB()
    srctrl.open(path)
    
    filename = '%s/test.c' % TMP_PATH
    with open(filename, 'w') as test:
        test.write('''
            int main(void) {
                return 0;
            }
        ''')
    
        file_id = srctrl.record_file(pathlib.Path(filename))
        assert file_id != None
        srctrl.record_file_language(file_id, 'C')
        assert True

    srctrl.close()

@pytest.fixture()
def test_record_symbol(test_create_db):
    path = '%s/db.srctrldb' % TMP_PATH

    # Open an existing database
    srctrl = SourcetrailDB()
    srctrl.open(path)
 
    hierarchy = NameHierarchy(
        NameHierarchy.NAME_DELIMITER_JAVA,
        [NameElement(
            '',
            'MyType',
            ''
        )]
    )
    # Insert a symbol once
    id_a = srctrl.record_symbol(hierarchy)
    assert(id_a != None)

    # Check that symbol exists
    assert(id_a == srctrl.get_symbol(hierarchy))
    
    srctrl.close()
    
def test_record_symbol_kind(test_record_symbol):
    path = '%s/db.srctrldb' % TMP_PATH

    # Open an existing database
    srctrl = SourcetrailDB()
    srctrl.open(path)

    hierarchy = NameHierarchy(
        NameHierarchy.NAME_DELIMITER_JAVA,
        [NameElement(
            '',
            'MyType',
            ''
        )]
    )
    # Insert a symbol once
    id_a = srctrl.record_symbol(hierarchy)
    assert(id_a != None)

    srctrl.record_symbol_kind(id_a, NodeType.NODE_CLASS)
    assert True 
    srctrl.close()

def test_record_symbol_kind(test_record_symbol):
    path = '%s/db.srctrldb' % TMP_PATH

    # Open an existing database
    srctrl = SourcetrailDB()
    srctrl.open(path)

    hierarchy = NameHierarchy(
        NameHierarchy.NAME_DELIMITER_JAVA,
        [NameElement(
            '',
            'MyType',
            ''
        )]
    )
    # Insert a symbol once
    id_a = srctrl.record_symbol(hierarchy)
    assert(id_a != None)

    srctrl.record_symbol_kind(id_a, NodeType.NODE_CLASS)
    assert True 
    srctrl.close()
    
def test_duplicate_symbol(test_create_db):
    path = '%s/db.srctrldb' % TMP_PATH

    # Open an existing database
    srctrl = SourcetrailDB()
    srctrl.open(path)
 
    # Insert a symbol once
    id_a = srctrl.record_symbol(NameHierarchy(
        NameHierarchy.NAME_DELIMITER_JAVA,
        [NameElement(
            '',
            'MyType',
            ''
        )]
    ))
    assert(id_a != None)
    
    # Insert the same symbol again
    id_b = srctrl.record_symbol(NameHierarchy(
        NameHierarchy.NAME_DELIMITER_JAVA,
        [NameElement(
            '',
            'MyType',
            ''
        )]
    ))
    assert(id_b != None)
    assert(id_a == id_b)

    srctrl.close()

