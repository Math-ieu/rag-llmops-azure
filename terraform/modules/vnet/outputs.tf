output "vnet_id" {
  value = azurerm_virtual_network.vnet.id
}

output "vnet_name" {
  value = azurerm_virtual_network.vnet.name
}

output "apps_subnet_id" {
  value = azurerm_subnet.apps_subnet.id
}
