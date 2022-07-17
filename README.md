# 👾 Ransomeware Simples

Trabalho para a disciplina de Segurança da Informação - PCS3544

## 🎈 Introdução

Este trabalho tem como objetivo demonstrar uma implmentação didática de um ransomware simples utilizando a linguagem Python.

A base para a implementação desse ransomware é a utilização de algoritmos de criptografia assimétricos, isso é importante para dar controle sobre a cifração para o "atacante". Dessa forma, uma chave pública será utilizada para a cifração no dispositivo da "vítima", enquanto a chave privada correspondente ficaria em posse do "atacante".

Devido à limitação do tamanho dos dados que algoritmos assimétricos conseguem cifrar, não seria possível cifrar grandes arquivos, deste modo, se utilizará criptografia simétrica para realizar a encriptação dos arquivos da "vítima". Porém, para garantir o controle sobre os dados encriptados ao "atacante", se utilizará criptografia assimétrica para encriptar a chave utilizada na encriptação com o algoritmo simétrico.

## 📚 Entendendo o funcionamento

Para realizar um ataque, algumas etapas têm que ser executadas antes, sendo elas as seguintes:

1. Gerar a chave pública do algoritmo assimétrico
2. Gerar a chave privada do algoritmo assimétrico

Já durante o ataque, as seguintes etapas têm que ser realizadas:

1. Gerar uma chave simétrica
2. Encriptar arquivos da "vítima" com a chave simétrica
3. Encriptar chave simétrica utilizando a chave pública assimétrica

Após o ataque ter sido concluído e a desencriptação tiver que ser realizadas, são executados os seguintes passos:

1. Desencriptar a chave simétrica utiliando a chave privada assimétrica
2. Desencriptar arquivos utlizando a chave simétrica

### Antes do ataque

Antes do ataque é necessário gerar as chaves que serão utilizadas pelo algoritmo de critografia assimétrico, para isso se utilizará a implementação do algoritmo RSA da biblioteca `cryptography` do Python.

#### Gerando a chave privada assimétricas

Primeramente é necessário realizar a importação dos métodos que serão utilizados na geração da chave.

```Python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
```

Para gerar a chave privada foi utilizada a função `rsa.generate_private_key`, definindo o `public_exponent` como `65537` e o tamanho da chave como `2048`.

> O `public_exponent` deve ser um número primo positivo, de preferência um número primo grande. Neste trabalho foi utilizado o número `65537` por ser o número normalmente utilizado em criptografias utilizando o RSA. Esse número é utilizado, principalmente, por razões históricas, uma vez que implementações anteriores do RAS em que expoentes muito pequenos eram utilizadas ficavam mais vuneráveis, enquanto a utilização de expoentes muito elevados exigiam um poder computacional muito grande. Esse número também é conhecido como o número de Fermat (Fn = 2^[2^(n)]+1), com n = 4.

```Python
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
```

Após gerar a chave, para utilizá-la porsteriormente é necessário serializá-la e salvá-la em um arquivo `.pem`.

```Python
serial_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open("private_asym_key.pem", "wb") as file:
    file.write(serial_private)
```

#### Gerando a chave pública assimétricas

### Método útil para durante e depois do ataque

### Durante o ataque

#### Gerando a chave simétricas

#### Encriptando os arquivos

#### Encriptando a chave simétrica

#### Execução completa

### Após o ataque

#### Decriptando a chave simétrica

#### Decriptando os arquivos

#### Execução completa

## 🚀 Utilizando os scripts
