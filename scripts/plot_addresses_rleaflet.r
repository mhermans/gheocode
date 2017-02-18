library(readr)
library(leaflet)
library(geojsonio)
library(RColorBrewer)

addr <- read_csv('projects/geocode_adressen/20172016_resultaten_woonenquete_adressen_geocoded.csv')

sectoren <- geojson_read('../geometries/geojson/sectoren.json', what = 'sp')
wijken <- geojson_read('../geometries/geojson/wijken_extended.json',
                       what = 'sp')

kaartje <- leaflet(sectoren) %>%
  addProviderTiles("CartoDB.Positron", group = "Kaart-laag") %>%
  addPolygons(weight = 0.5, color='black', group = "Sector-laag")

# sector_popups <- paste0(
#   "<strong>Gemeente: </strong>", sp.sectoren@data$gemeente,
#   "<br/><strong>Sector-naam: </strong>", sp.sectoren@data$sector.nl, 
#   "<br/><strong>Sector-code: </strong>", sp.sectoren@data$cs012011,
#   "<br/><strong>Sector-categorie: </strong>", sp.sectoren@data$CD_SECTOR,
#   "<br/><strong>Selectie-wijze: </strong>", sp.sectoren@data$kleur)

kaartje <- kaartje %>% 
  addPolygons(
    data=wijken, 
    group = "Wijk-laag",
    fillOpacity = 0.5,
    weight=3,
    color='grey',
    # popup = sector_popups,
    fillColor = brewer.pal(12, 'Set3'))

# Voeg legende & kaart-laag controle toe
# kaartje <- kaartje %>% 
#   addLegend(position = 'bottomright',opacity = 0.4, 
#             colors = brewer.pal(4, 'Paired')[c(2,1,4)], 
#             labels = c('Centrumstad (steekproef)', 'Centrumstad (selectie)', 'Volledige stad/gemeente'),
#             title = 'Manier van selecteren sectoren') %>%
#   addLayersControl(position = 'bottomright',
#                    # baseGroups = c("Topographical", "Road map", "Satellite"),
#                    overlayGroups = c("Kaart-laag", "Gemeente-laag", "Sector-laag"),
#                    options = layersControlOptions(collapsed = FALSE))
# 
# 
# # sla kaartje op als html-pagina (pas bestandsnaam aan voor andere locatie)
# saveWidget(kaartje, 'map_sectoren_basic.html')