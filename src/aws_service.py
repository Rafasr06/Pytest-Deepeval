import boto3

def salvar_arquivo_s3(
        bucket: str,
        chave: str,
        conteudo: str
):

    client = boto3.client("s3")
    client.put_object(
        Bucket=bucket,
        Key=chave,
        Body=conteudo
    )

    return True
