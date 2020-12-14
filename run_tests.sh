# run using: source run_tests.sh
dropdb magic_the_gathering_test
createdb magic_the_gathering_test
psql magic_the_gathering_test < test_db.pgsql
echo "----- Done Setup -----"
echo "----- Running Tests -----"
python test_flaskr.py
