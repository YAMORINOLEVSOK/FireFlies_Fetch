# Fetch Fireflies Transcripts

> **Ferramenta para baixar todas as transcrições do Fireflies.ai via API GraphQL, com texto separado por falante.**

---

## 📋 Descrição

Este projeto automatiza o download em massa de transcrições do Fireflies.ai, facilitando o acesso aos dados de reuniões para análise, processamento ou backup. A ferramenta utiliza a API GraphQL oficial do Fireflies para extrair transcrições com identificação de falantes.

### ✨ Funcionalidades

| Recurso | Descrição |
| ------- | --------- |
| 🔄 **Download em massa** | Baixa automaticamente todas as transcrições da sua conta via API GraphQL |
| 🗣️ **Identificação de falantes** | Preserva os rótulos de quem falou cada trecho (`Nome: texto`) |
| 💾 **Organização automática** | Salva cada transcrição como `<titulo>_<id>.txt` no diretório `output/` |
| ♻️ **Retomada inteligente** | Ignora arquivos já baixados, permitindo executar novamente sem duplicar |
| ⚠️ **Tratamento de erros** | Lida com transcrições indisponíveis ou em processamento sem interromper a execução |
| 📊 **Scripts auxiliares** | Inclui ferramentas para contagem e análise de discrepâncias |

---

## 🔧 Requisitos

- **Python 3.8+** ([python.org](https://python.org))
- **Token API do Fireflies.ai** (plano Pro/Business ou superior)
- Biblioteca `requests` (instalada automaticamente via requirements.txt)

> **Nota:** Planos gratuitos não expõem o menu de token da API. É possível usar o cookie `token` como alternativa, mas o token oficial é recomendado.

---

## 🚀 Instalação e Uso

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/Fetch-Fireflies-Transcripts.git
cd Fetch-Fireflies-Transcripts
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o token da API

Você precisa obter seu token da API do Fireflies:

1. Acesse [app.fireflies.ai](https://app.fireflies.ai)
2. Vá em **Settings › Integrations**
3. Role até **Developer / API** e clique em **Generate Token**
4. Copie o token gerado

Configure o token como variável de ambiente:

**Windows (PowerShell):**
```powershell
$env:FIREFLIES_TOKEN="seu-token-aqui"
```

**Windows (CMD):**
```cmd
set FIREFLIES_TOKEN=seu-token-aqui
```

**Linux/Mac:**
```bash
export FIREFLIES_TOKEN="seu-token-aqui"
```

### 5. Execute o script principal

```bash
python fireflies_fetch_script
```

O script irá:
- Paginar por todas as suas transcrições
- Baixar cada uma no formato `output/<titulo>_<id>.txt`
- Exibir o progresso no terminal
- Pular arquivos já existentes

### Exemplo de saída:

```
⬇︎  saved Reunião Cliente XYZ - 2024-05-01_a1b2c3d4.txt
✔︎  Kickoff Call - 2024-04-18_e5f6g7h8.txt exists; skipping
⚠️  Weekly Sync: object_not_found – skipped

✅  Done! Transcripts in → C:\Users\...\output
```

---

## 📂 Estrutura do Projeto

```
Fetch-Fireflies-Transcripts/
├── fireflies_fetch_script      # Script principal de download
├── _count_total.py              # Contador de transcrições totais
├── analyze_discrepancies.py    # Análise de discrepâncias (opcional)
├── build_calendar.py            # Construtor de calendário (opcional)
├── requirements.txt             # Dependências Python
├── README.md                    # Este arquivo
├── .gitignore                   # Arquivos ignorados pelo Git
└── output/                      # Diretório de saída (não versionado)
    └── (suas transcrições aqui)
```

---

## 🛠️ Scripts Auxiliares

### `_count_total.py`
Conta o número total de transcrições disponíveis na API sem baixá-las.

```bash
python _count_total.py
```

### `analyze_discrepancies.py`
Compara um calendário de aulas planejadas com as transcrições baixadas para identificar discrepâncias de professores.

**Requer:**
- Arquivo CSV com calendário de aulas em `Files/calendario_aulas.csv`
- Transcrições em `output/`

```bash
python analyze_discrepancies.py
```

### `build_calendar.py`
Constrói um calendário formatado a partir de uma planilha de alocação.

**Requer:**
- Arquivo CSV de entrada em `Files/`

```bash
python build_calendar.py
```

---

## ⚙️ Configurações Avançadas

Você pode ajustar o comportamento do script editando as variáveis no início do arquivo `fireflies_fetch_script`:

| Variável | Padrão | Descrição |
| -------- | ------ | --------- |
| `PAGE_SIZE` | 50 | Número de transcrições por página (máximo: 50) |
| `OUT_DIR` | `output` | Diretório de destino dos arquivos |
| `time.sleep(0.2)` | 0.2s | Intervalo entre requisições (ajuste se necessário) |

---

## 🐛 Solução de Problemas

| Problema | Possível Causa | Solução |
| -------- | -------------- | ------- |
| `RuntimeError: Unauthorized` | Token inválido ou expirado | Regenere o token e configure novamente |
| `TOKEN_MISSING` | Variável de ambiente não configurada | Execute o comando `set` ou `export` com seu token |
| Nenhuma transcrição baixada | Workspace vazio ou conta errada | Verifique se há reuniões na sua conta Fireflies |
| `KeyError: 'sentences'` | API retorna formato diferente | Sua conta pode usar `segments` em vez de `sentences` |

---

## 📝 Observações

- **Privacidade:** Os arquivos de transcrição não são incluídos no repositório por padrão (`.gitignore`)
- **Uso educacional:** Este projeto foi desenvolvido para uso acadêmico e administrativo
- **API Rate Limits:** O script inclui delays entre requisições para respeitar limites da API

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

---

## 📄 Licença

MIT License - Sinta-se livre para usar e modificar conforme necessário.

---

## 🙏 Créditos

- Ideia original e primeiro script por **[Leslie Barry](https://lesliebarry.substack.com/p/solved-firefliesai-bulk-transcript)**
- Adaptação e melhorias para uso educacional

---

**Desenvolvido para automação de processos educacionais** 🎓
