find ./conversations/migrations/* ! -name "__init__.py" -delete
find ./core/migrations/* ! -name "__init__.py" -delete
find ./lists/migrations/* ! -name "__init__.py" -delete
find ./reservations/migrations/* ! -name "__init__.py" -delete
find ./reviews/migrations/* ! -name "__init__.py" -delete
find ./rooms/migrations/* ! -name "__init__.py" -delete
find ./users/migrations/* ! -name "__init__.py" -delete
echo "성공!"
