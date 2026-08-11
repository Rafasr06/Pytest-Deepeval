from aws_service import salvar_arquivo_s3

def test_salvar_arquivo_s3(mocker):
    mock_client = mocker.MagicMock()

    mocker.patch('aws_service.boto3.client', return_value=mock_client)

    resultado = salvar_arquivo_s3(
        bucket="bucket-teste",
        chave="arquivo.txt",
        conteudo="Teste AWS S3"
    )

    assert resultado is True

    mock_client.put_object.assert_called_once_with(
        Bucket="bucket-teste",
        Key="arquivo.txt",
        Body="Teste AWS S3"
    )
