#!/bin/bash
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi
npx wrangler pages deploy ./dist --project-name journeystorm --branch main
