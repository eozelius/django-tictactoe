document.addEventListener("DOMContentLoaded", function() {
  var gameDetailForm = document.querySelector('#game_detail_form')

  if (gameDetailForm) {
    var cells = document.querySelectorAll('.game-detail-container td')

    cells.forEach(cell => {
      cell.addEventListener('click', function (event) {
        var row = event.target.parentElement.dataset.row
        var col = event.target.dataset.col
        var content = event.target.textContent.replace(/^\s+|\s+$/g,'')

        // Ensure cell is empty
        if (content !== '') { return }

        // Set form inputs and submit
        gameDetailForm.querySelector('input.game-detail__row').value = row
        gameDetailForm.querySelector('input.game-detail__col').value = col
        gameDetailForm.submit()
      })
    })
  }
})