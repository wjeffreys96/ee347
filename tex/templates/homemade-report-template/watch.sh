inotifywait -m -r --exclude './build|watch.sh|build.sh' -e close_write . | while read -r file; do
  ./build.sh
done
