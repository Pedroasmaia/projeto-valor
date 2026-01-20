# ScoutGuard

A **ScoutGuard** é uma extensão do Azure DevOps que adiciona uma task para executar o Docker Scout após o `docker build`, gerando um relatório JSON de CVEs.

## Conteúdo

- Task do Azure DevOps para rodar `docker scout cves`.
- Instalação automática do Docker Scout (opcional).
- Exporta o caminho do relatório via variável `ScoutGuardReportPath`.

## Pré-requisitos

- Docker instalado no agente.
- Acesso à internet se precisar instalar o Docker Scout.

## Inputs da task

| Input | Obrigatório | Descrição |
| --- | --- | --- |
| `imageName` | Sim | Nome/tag da imagem Docker (ex: `minha-imagem:latest`). |
| `outputPath` | Sim | Caminho para salvar o JSON (relativo ao workspace ou absoluto). |
| `installScout` | Sim | Instala o Docker Scout automaticamente se necessário. |
| `additionalArgs` | Não | Argumentos extras para `docker scout cves`. |

## Exemplo de uso (YAML)

```yaml
- task: ScoutGuard@0
  inputs:
    imageName: 'minha-imagem:latest'
    outputPath: '$(Build.ArtifactStagingDirectory)/scout-report.json'
    installScout: true
```

## Empacotar

```bash
npm install
npm install -g tfx-cli
cd ScoutGuard
npm install --prefix tasks/scoutguard
npx tfx extension create --manifest-globs vss-extension.json
```

## Publicar

```bash
npx tfx extension publish --vsix scoutguard-0.1.0.vsix --publisher seu-publicador
```
