# Configuração do Google Drive MCP para Cursor

Devido a limitações de PATH no Windows, vamos usar Python diretamente para rodar o servidor MCP.

## Passo 1: Criar Credenciais OAuth do Google

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a **Google Drive API**:
   - Vá para "APIs & Services" > "Library"
   - Busque "Google Drive API" e clique em "Enable"
4. Configure a tela de consentimento OAuth:
   - Vá para "APIs & Services" > "OAuth consent screen"
   - Escolha "External" (ou "Internal" se for Google Workspace)
   - Preencha nome do app, email de suporte
   - Adicione seu email como usuário de teste
5. Crie credenciais OAuth:
   - Vá para "APIs & Services" > "Credentials"
   - Clique "Create Credentials" > "OAuth client ID"
   - Tipo de aplicação: **Desktop app**
   - Dê um nome (ex: "Google Drive MCP")
   - Clique "Create"
6. **Copie o Client ID e Client Secret** que aparecem

## Passo 2: Instalar o Servidor Google Workspace MCP

Abra um novo PowerShell (como Administrador se necessário) e execute:

```powershell
# Navegar para uma pasta de trabalho
cd "$env:USERPROFILE\Documents"

# Clonar o repositório
git clone https://github.com/taylorwilsdon/google_workspace_mcp.git
cd google_workspace_mcp

# Criar ambiente virtual Python
python -m venv venv_gwmcp

# Ativar o ambiente virtual (bypass execution policy se necessário)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\venv_gwmcp\Scripts\Activate.ps1

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

Se não houver `requirements.txt`, instale manualmente:
```powershell
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client fastapi uvicorn pydantic
```

## Passo 3: Configurar Variáveis de Ambiente

Defina as credenciais OAuth:

```powershell
$env:GOOGLE_OAUTH_CLIENT_ID="seu-client-id-aqui.apps.googleusercontent.com"
$env:GOOGLE_OAUTH_CLIENT_SECRET="seu-client-secret-aqui"
```

## Passo 4: Testar o Servidor

```powershell
# Modo stdio (para MCP)
python main.py --tools drive

# Ou modo HTTP (mais fácil de debugar)
python main.py --transport streamable-http --tools drive
```

No primeiro uso, uma janela de autenticação abrirá. Faça login e autorize o acesso.

## Passo 5: Configurar Cursor

### Opção A: Modo STDIO (Recomendado)

Abra Cursor: **Settings > Features > MCP > Edit Config**

Adicione ao arquivo de configuração:

```json
{
  "mcpServers": {
    "google_drive": {
      "command": "C:\\Users\\[SEU_USUARIO]\\Documents\\google_workspace_mcp\\venv_gwmcp\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\[SEU_USUARIO]\\Documents\\google_workspace_mcp\\main.py",
        "--tools",
        "drive"
      ],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "seu-client-id-aqui.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "seu-client-secret-aqui"
      }
    }
  }
}
```

**Importante**: Substitua `[SEU_USUARIO]` pelo seu nome de usuário Windows.

### Opção B: Modo HTTP (Alternativa)

1. Mantenha o servidor rodando em um terminal:
   ```powershell
   cd C:\Users\[SEU_USUARIO]\Documents\google_workspace_mcp
   .\venv_gwmcp\Scripts\Activate.ps1
   python main.py --transport streamable-http --tools drive
   ```

2. No Cursor, configure:
   ```json
   {
     "mcpServers": {
       "google_drive": {
         "command": "npx",
         "args": ["-y", "mcp-remote", "http://localhost:8000/mcp"]
       }
     }
   }
   ```

## Passo 6: Verificar Funcionamento

1. Reinicie o Cursor
2. Abra o Command Palette (Ctrl+Shift+P)
3. Digite "MCP" e veja se o servidor `google_drive` aparece
4. Tente usar comandos como:
   - "Liste os arquivos no meu Google Drive"
   - "Busque documentos com o nome X"
   - "Leia o conteúdo do arquivo Y"

## Ferramentas Disponíveis (Drive)

- `search_drive_files`: Buscar arquivos
- `get_drive_file_content`: Ler conteúdo de arquivos
- `list_drive_items`: Listar itens de uma pasta
- `create_drive_file`: Criar novos arquivos

## Troubleshooting

### Erro de autenticação
- Verifique se as credenciais OAuth estão corretas
- Certifique-se de ter autorizado o app no navegador
- Verifique se a API do Google Drive está ativada

### Servidor não inicia
- Confirme que todas as dependências foram instaladas
- Verifique os logs de erro no terminal
- Tente rodar com `--transport streamable-http` para ver mensagens mais claras

### Cursor não encontra o servidor
- Verifique os caminhos absolutos no arquivo de configuração
- Teste o comando manualmente no PowerShell
- Reinicie o Cursor após mudanças na configuração

