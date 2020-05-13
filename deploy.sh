#!/usr/bin/env bash
PROJECT_ID=oca-k8
gcloud builds submit --tag gcr.io/${PROJECT_ID}/gv-activemq-proxy
gcloud run deploy --image gcr.io/${PROJECT_ID}/gv-activemq-proxy --platform managed
