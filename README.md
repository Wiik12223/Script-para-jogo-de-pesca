Ótimo\! Abaixo está o arquivo `README.md` formatado para o seu projeto de automação de pesca. Ele inclui as instruções de uso, calibração e solução de problemas para o código fornecido.

# 🎣 FishBot - Automação de Pesca

Este script em Python automatiza o minigame de pesca em jogos que utilizam o sistema de "manter a barra" para captura. Ele utiliza visão computacional (`OpenCV`) para rastrear o peixe e o controle do mouse (`PyAutoGUI`) para manter a mira na área alvo.

## ⚠️ Aviso Importante

O uso de scripts de automação (bots) pode violar os Termos de Serviço de alguns jogos, incluindo o Roblox. Use este script por sua conta e risco.

## 🚀 Instalação e Configuração

### 1\. Pré-requisitos

Certifique-se de ter o **Python (versão 3.8 a 3.11 é recomendada)** instalado no seu sistema.

### 2\. Instalação das Bibliotecas

Abra seu terminal ou Prompt de Comando e instale as bibliências necessárias:

```bash
pip install pyautogui opencv-python numpy
```

### 3\. Arquivos de Template (Imagens)

O script depende de três imagens (templates) para identificar os elementos na tela. Coloque todas na **mesma pasta** do seu script Python:

| Variável | Nome do Arquivo | Descrição |
| :--- | :--- | :--- |
| `TEMPLATE_MINIGAME` | `template_hold_click.png` | Imagem recortada do texto **"HOLD CLICK"**. Usada para iniciar o controle. |
| `TEMPLATE_PEIXE_BRANCO` | `template_peixe_branco.png` | Imagem recortada do **peixe na cor branca**. |
| `TEMPLATE_PEIXE_VERDE` | `template_peixe_verde.png` | Imagem recortada do **peixe na cor verde** (quando está sendo rastreado pela barra). |

-----

## ⚙️ Calibração (Ajuste Obrigatório)

Antes de rodar o bot, você deve ajustar as coordenadas para sua tela e jogo. Edite as variáveis no início do arquivo Python:

### 1\. Coordenadas de Lançamento

Ajuste estas coordenadas para o ponto exato onde você clica no mar para lançar a vara.

```python
PONTO_LANCAMENTO_X = 900  # Coordenada X (Horizontal) na sua tela
PONTO_LANCAMENTO_Y = 500  # Coordenada Y (Vertical) na sua tela
```

### 2\. Posição Alvo (Y\_CENTRO\_ALVO)

O script usa a localização do texto "HOLD CLICK" como referência. O `Y_CENTRO_ALVO` é um **offset** (deslocamento) que você deve medir:

1.  Observe o minigame: Qual a coordenada Y do texto "HOLD CLICK"?
2.  Qual a coordenada Y do **centro ideal** da barra de pesca azul (o ponto onde o peixe deve ser mantido)?
3.  O `Y_CENTRO_ALVO` é a diferença entre eles (Centro Ideal - Posição do "HOLD CLICK").

<!-- end list -->

```python
Y_CENTRO_ALVO = local_minigame[1] + 100  # <--- AJUSTE ESTE NÚMERO!
```

*Se o centro da barra estiver 150 pixels abaixo do texto "HOLD CLICK", use `+ 150`.*

### 3\. Sensibilidade

Ajuste a margem de erro para o controle do mouse:

```python
MARGEM_CONTROLE = 15  # Diminua (ex: para 10) para tornar o controle mais sensível/rápido.
```

-----

## ▶️ Como Executar

1.  Abra o jogo de pesca na tela.
2.  Execute o script no seu terminal:

<!-- end list -->

```bash
python seu_script.py
```

3.  Para **PARAR** o script a qualquer momento, pressione `Ctrl + C` no terminal.

## 🔧 Lógica de Funcionamento

1.  **Loop Principal:** O script verifica constantemente a tela em busca do template `template_hold_click.png`.
2.  **Lançamento:** Se o `template_hold_click.png` **NÃO** for encontrado, ele clica nas coordenadas (`PONTO_LANCAMENTO_X`, `Y`) para lançar a vara.
3.  **Controle da Pesca:** Se o `template_hold_click.png` **FOR** encontrado, o script entra no loop de controle:
      * Ele procura simultaneamente por `template_peixe_branco.png` ou `template_peixe_verde.png`.
      * **Se o peixe estiver ABAIXO do `Y_CENTRO_ALVO`:** O script **segura** o botão esquerdo do mouse para subir a barra.
      * **Se o peixe estiver ACIMA do `Y_CENTRO_ALVO`:** O script **solta** o botão esquerdo do mouse para descer a barra.
4.  **Fim da Pesca:** Quando nenhum dos templates do peixe/minigame for encontrado, o script solta o mouse e volta ao loop de lançamento.
