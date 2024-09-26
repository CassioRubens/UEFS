import os
from qgis.core import QgsRasterLayer, QgsProject
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry

def calcular_area_pixel(layer):
    # Verifica se a camada é válida
    if not layer or not isinstance(layer, QgsRasterLayer):
        print("Camada inválida ou não é uma camada raster.")
        return None
    
    # Obtém a resolução X e Y (em metros)
    res_x = layer.rasterUnitsPerPixelX()
    res_y = layer.rasterUnitsPerPixelY()
    
    # Verifica se a resolução foi obtida corretamente
    if res_x is None or res_y is None:
        print(f"Não foi possível obter a resolução da camada: {layer.name()}")
        return None
    
    # Calcula a área do pixel em km²
    area_pixel_km2 = (res_x * res_y) / 1_000_000
    
    # Print dos valores de resolução e área por pixel
    print(f"Resolução X: {res_x} metros/pixel, Resolução Y: {res_y} metros/pixel")
    print(f"Área de pixel em km²: {area_pixel_km2:.6f} km²")
    
    return area_pixel_km2

# ID da camada raster
camada_id = "Fig0112_4__4th_from_top_South_Amer__3e721e28_cfaa_498e_9d74_5e4bc913ffc7"

# Carregar a camada de imagem
camada = QgsProject.instance().mapLayer(camada_id)

if not camada:
    raise ValueError(f"Camada com ID {camada_id} não encontrada.")

# Calcular a área de pixel da camada
area_pixel = calcular_area_pixel(camada)

if not area_pixel:
    raise ValueError("Não foi possível calcular a área do pixel para a camada fornecida.")

# Obter dimensões da camada (MxN)
width = camada.width()
height = camada.height()
total_pixels = width * height

# Print do tamanho da imagem
print(f"Tamanho da imagem: {width} x {height} pixels (M x N)")
print(f"Total de pixels: {total_pixels}")

# Configurar a entrada para a Calculadora Raster
calc_entry = QgsRasterCalculatorEntry()
calc_entry.raster = camada
calc_entry.bandNumber = 1  # Usando a banda 1
calc_entry.ref = 'layer@1'

# Definir a expressão para multiplicar os valores de cinza pela área do pixel
expression = f"layer@1 * {area_pixel}"

# Print da expressão a ser utilizada
print(f"Expressão usada na calculadora raster: {expression}")

# Configurar e rodar a Calculadora Raster
output_path = "/home/cassiorubens/output.tif"
calc = QgsRasterCalculator(
    expression, 
    output_path, 
    "GTiff", 
    camada.extent(),  # Usar a extensão da camada
    width,   # Usar a largura da camada
    height,  # Usar a altura da camada
    [calc_entry]
)

# Processar o cálculo e salvar a saída
result = calc.processCalculation()

# Verificar se o cálculo foi bem-sucedido
if result == 0:  # 0 indica sucesso
    print("Processamento bem-sucedido. Raster salvo em:", output_path)
else:
    print("Erro ao processar a Calculadora Raster.")
