window.onload = () => {
  const moneySelect = document.getElementById('money_name')
  const moneyValue = document.getElementById('money_value')
  moneySelect.addEventListener('change', function(e) {
    if (this.selectedIndex !== 0) {
      const price = this.children[this.selectedIndex].dataset.price * 1
      moneyValue.value = price.toFixed(2)
    } else if (this.selectedIndex !== 0) {
      moneyValue.value = 'Prix d\'achat'
    }
  })
}