mkdir -p assets/js/bootstrap assets/css/bootstrap
cp node_modules/bootstrap/dist/js/bootstrap.bundle.min.js assets/js/bootstrap
cp node_modules/bootstrap/dist/js/bootstrap.bundle.min.js.map assets/js/bootstrap
cp node_modules/bootstrap/dist/css/bootstrap.min.css assets/css/bootstrap

mkdir -p assets/css/bootstrap-icons static/css/bootstrap-icons/
cp node_modules/bootstrap-icons/font/bootstrap-icons.min.css assets/css/bootstrap-icons
cp -r node_modules/bootstrap-icons/font/fonts static/css/bootstrap-icons
