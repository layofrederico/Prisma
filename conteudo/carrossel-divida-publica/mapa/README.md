# Mapa do slide "A dívida nasceu com o Brasil"

Contornos reais de Brasil, Reino Unido e Irlanda a partir do Natural Earth 1:50m, na distribuição
TopoJSON `world-atlas@2.0.2` (`countries-50m.json`, não versionado aqui — `mapa.py` baixa via
jsdelivr). O script decodifica o TopoJSON, projeta em equiretangular corrigida pelo cosseno da
latitude central e simplifica com Douglas-Peucker.

Brasil (8,5 px/grau) e ilhas britânicas (20 px/grau) estão em **escalas diferentes**: é ilustração
da viagem, não mapa em escala — em escala única o Reino Unido ficaria com cerca de 30 px.
