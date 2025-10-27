import pyautogui
import cv2
import numpy as np
import time

# --- CONFIGURAÇÕES GLOBAIS ---
# Ajuste conforme a sua tela e o jogo
MARGEM_CONTROLE = 15  # Margem de pixels para manter o peixe no centro da barra.
TEMPO_ESPERA_LANCAMENTO = 10.0  # Tempo para esperar o minigame aparecer após o clique.
PONTO_LANCAMENTO_X = 900  # Coordenada X da tela para clicar no mar e lançar a vara.
PONTO_LANCAMENTO_Y = 500  # Coordenada Y da tela para clicar no mar e lançar a vara.

# Nomes dos arquivos de template (DEVE ESTAR NA MESMA PASTA DO SCRIPT!)
# Nomes dos arquivos de template
TEMPLATE_MINIGAME = 'template_hold_click.png' # Use o template do "HOLD CLICK"
TEMPLATE_PEIXE_BRANCO = 'template_peixe_branco.png'       # Template do peixe branco
TEMPLATE_PEIXE_VERDE = 'template_peixe_verde.png'         # NOVO: Template do peixe verde

def buscar_template(template_paths, threshold=0.8):
    """
    Busca um ou múltiplos templates na tela e retorna a melhor localização do PRIMEIRO encontrado.
    template_paths pode ser um único path (string) ou uma lista de paths (list of strings).
    """
    if isinstance(template_paths, str):
        template_paths = [template_paths] # Transforma em lista se for um único path

    try:
        screenshot = pyautogui.screenshot()
        screen_np = np.array(screenshot)
        screen_cv = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

        for template_path in template_paths:
            template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
            if template is None:
                print(f"ERRO: Não foi possível carregar o template: {template_path}")
                continue # Tenta o próximo template na lista

            w, h = template.shape[1], template.shape[0]
            res = cv2.matchTemplate(screen_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val >= threshold:
                top_left = max_loc
                center_x = top_left[0] + w // 2
                center_y = top_left[1] + h // 2
                # Retorna a coordenada central do objeto encontrado e o valor de confiança
                return (center_x, center_y), max_val
        
        return None, 0.0 # Nenhum template encontrado com a confiança necessária

    except Exception as e:
        print(f"Erro na busca de template: {e}")
        return None, 0.0

def controlar_pesca(y_peixe, y_centro_alvo):
    """
    Controla o clique do mouse para manter o peixe no centro da barra azul.
    """
    if y_peixe is None:
        # Se o peixe não for encontrado, solta o mouse como segurança
        pyautogui.mouseUp(button='left')
        return

    # Ajuste: A coordenada Y aumenta de cima para baixo.
    # Se Y_Peixe < Y_Centro, o peixe está *acima* do centro, precisamos soltar o mouse (cair).
    if y_peixe < y_centro_alvo - MARGEM_CONTROLE:
        if pyautogui.mouseDown(button='left', _pause=False):
             # Apenas solta o botão se já estiver pressionado
             pyautogui.mouseUp(button='left')
             print("AÇÃO: Soltar (Peixe muito alto)")
        else:
             pyautogui.mouseUp(button='left')
             print("AÇÃO: Soltar (Peixe muito alto)")


    # Se Y_Peixe > Y_Centro, o peixe está *abaixo* do centro, precisamos segurar o mouse (subir).
    elif y_peixe > y_centro_alvo + MARGEM_CONTROLE:
        pyautogui.mouseDown(button='left')
        print("AÇÃO: Segurar (Peixe muito baixo)")

    # Se estiver dentro da margem, o controle é mantido no estado atual
    else:
        # Para maior estabilidade, se estiver no centro, tenta segurar por um momento
        # para reagir à queda iminente (que é mais rápida que a subida).
        print("AÇÃO: Manter (Na mira)")
        pass # Mantém o estado atual (se estava segurando, continua; se estava solto, continua)
             # Você pode experimentar com pequenos cliques rápidos aqui se a estabilidade for baixa.


def main():
    """
    Loop principal do script de automação.
    """
    print("Iniciando script de automação de pesca...")
    print("Pressione CTRL + C no console a qualquer momento para PARAR o script.")

    try:
        while True:
            # --- 1. VERIFICAR STATUS DO MINIGAME ---
            
            # Tenta encontrar a imagem do minigame na tela
            local_minigame, conf_minigame = buscar_template(TEMPLATE_MINIGAME, threshold=0.7)

            if local_minigame:
                print("\nSTATUS: Minigame detectado. Iniciando controle de pesca...")
                
                # --- 2. LOOP DE PESCA (MINIGAME ATIVO) ---
                
                # Calibrar o centro Y da barra azul. 
                # ESTE VALOR PRECISA SER AJUSTADO MANULAMENTE.
                # Use as coordenadas Y do minigame e adicione um offset para o centro da barra.
                # Exemplo: O minigame começa em (500, 300), a barra está 50 pixels abaixo, e a barra tem 200 de altura.
                # Y_CENTRO_ALVO seria 300 + 50 + 100 = 450.
                Y_CENTRO_ALVO = local_minigame[1] + 150  # Exemplo de offset. **AJUSTAR!**
                
                # Loop interno para o controle do minigame (execução rápida)
                for i in range(5000): # Roda por um tempo, o loop irá parar se o minigame sumir.
                    
                    local_peixe, conf_peixe = buscar_template([TEMPLATE_PEIXE_BRANCO, TEMPLATE_PEIXE_VERDE], threshold=0.9)
                    
                    if local_peixe:
                        y_peixe = local_peixe[1]
                        controlar_pesca(y_peixe, Y_CENTRO_ALVO)
                        # Reação rápida (quanto menor, mais rápido reage, mas mais CPU consome)
                        time.sleep(0.01) # 10 milissegundos
                    else:
                        # O peixe/minigame sumiu (Pesca concluída ou falha de detecção)
                        print("FIM DE JOGO: Peixe ou minigame não detectado.")
                        pyautogui.mouseUp(button='left') # Garante que o mouse está solto
                        time.sleep(TEMPO_ESPERA_LANCAMENTO) # Espera antes de relançar
                        break # Volta para o loop principal para relançar
                        
            else:
                # --- 3. LANÇAR A VARA ---
                print("STATUS: Minigame não detectado. Lançando a vara...")
                
                pyautogui.mouseUp(button='left') # Garante que está solto antes de clicar
                pyautogui.click(x=PONTO_LANCAMENTO_X, y=PONTO_LANCAMENTO_Y, button='left')
                
                print(f"VARAS LANÇADA em ({PONTO_LANCAMENTO_X}, {PONTO_LANCAMENTO_Y}). Aguardando {TEMPO_ESPERA_LANCAMENTO}s...")
                time.sleep(TEMPO_ESPERA_LANCAMENTO)


    except KeyboardInterrupt:
        print("\nScript PARADO pelo usuário (CTRL+C). Finalizando...")
        pyautogui.mouseUp(button='left') # Garante que o mouse não fique preso.
        exit()

if __name__ == "__main__":
    main()