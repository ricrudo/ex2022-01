Arreglo definitivo: recompilar Python enlazando un OpenSSL “real”

1) Instala OpenSSL 1.1 en tu home

mkdir -p ~/src && cd ~/src

curl -O -L https://www.openssl.org/source/openssl-1.1.1w.tar.gz

tar xzf openssl-1.1.1w.tar.gz

cd openssl-1.1.1w

./Configure darwin64-x86_64-cc --prefix=$HOME/opt/openssl-1.1 --openssldir=$HOME/opt/openssl-1.1

make -j4

make install

2) Descargar python 3.9.21

cd ~/src

curl -O -L https://www.python.org/ftp/python/3.9.21/Python-3.9.21.tgz

tar xzf Python-3.9.21.tgz

cd Python-3.9.21

Catalina es Intel, así que darwin64-x86_64-cc aplica.

3) Reconfigura y recompila Python 3.9.21 usando ese OpenSSL
cd ~/src/Python-3.9.21   # ajusta a la ruta donde tengas las fuentes

make distclean || true

export CPPFLAGS="-I$HOME/opt/openssl-1.1/include"

export LDFLAGS="-L$HOME/opt/openssl-1.1/lib -Wl,-rpath,$HOME/opt/openssl-1.1/lib"

export PATH="$HOME/opt/openssl-1.1/bin:$PATH"

./configure --with-openssl="$HOME/opt/openssl-1.1" --enable-optimizations
make -j4
sudo make altinstall
