#!/bin/bash

# 使用方式: ./run.sh [build|start|restart|down|clean]

ACTION=$1

function open_browser() {
  URL="http://localhost:8501"
  echo "🌐 Opening $URL in your browser..."

  if which xdg-open > /dev/null; then
    xdg-open "$URL"
  elif which open > /dev/null; then
    open "$URL"
  elif which start > /dev/null; then
    start "$URL"
  else
    echo "❗ Could not detect browser opening command. Please open $URL manually."
  fi
}

function build() {
  echo "🔧 Building all Docker containers..."
  docker-compose build
}

function start() {
  echo "🚀 Starting all services..."
  docker-compose up -d
  open_browser
}

function restart() {
  echo "🔁 Restarting services..."
  docker-compose down
  docker-compose up -d --build
  open_browser
}

function down() {
  echo "🛑 Stopping all containers..."
  docker-compose down
}

function clean() {
  echo "🧹 Cleaning up containers and dangling images..."
  docker-compose down --volumes --remove-orphans
  docker image prune -f
}

function help() {
  echo "Usage: ./run.sh [build|start|restart|down|clean]"
}

case "$ACTION" in
  build)
    build
    ;;
  start)
    start
    ;;
  restart)
    restart
    ;;
  down)
    down
    ;;
  clean)
    clean
    ;;
  *)
    help
    ;;
esac