$(document).ready(function () {
  // Attach click event to category links
  $('.category-item a').click(function (event) {
    event.preventDefault();
    var category = $(this).data('category');

    // Update the selected_category variable
    selected_category = category;

    // Perform any additional logic or actions with the updated selected_category variable

    // Update the displayed text    
    $('#selected-category').text(selected_category);
  });

  // Get the search input element
  const searchInput = document.getElementById('category-search');

  // Get all category items
  const categoryItems = document.querySelectorAll('.category-item');

  // Function to filter the categories
  const filterCategories = (searchTerm) => {
    const term = searchTerm.toLowerCase();
    categoryItems.forEach((item) => {
      const categoryButton = item.querySelector('button');
      const category = categoryButton.textContent.toLowerCase();
      if (category.includes(term)) {
        item.style.display = 'block';
      } else {
        item.style.display = 'none';
      }
    });
  };

  // Event listener for input changes
  searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value;
    filterCategories(searchTerm);
  });

  function rateStar(num, starsContainer) {
    const stars = starsContainer.querySelectorAll(".star");

    stars.forEach((star, index) => {
      if (index < num) {
        star.classList.add("filled");
      } else {
        star.classList.remove("filled");
      }
    });
  }

  // Attach event listener to each star icon within each book card
  const bookCards = document.querySelectorAll(".bk-dsp .card");

  bookCards.forEach((card) => {
    const stars = card.querySelectorAll(".far.fa-star");
    const starsContainer = card.querySelector(".bk-stars");

    stars.forEach((star, index) => {
      star.addEventListener("click", () => {
        rateStar(index + 1, starsContainer);
      });
    });
  });

  // For the likes
  hearts = document.querySelectorAll('.fa-heart')
  hearts.forEach(heart => {
    heart.addEventListener('click', () => {
      // Toggle the 'active' class
      heart.classList.toggle('red');
    });
  });

  $('#form1').on('input', function () {
    var query = $(this).val().toLowerCase();
    var searchBy = $('#search-by').val(); // Get the selected search option

    // Filter the books based on the search query and search option
    var filteredBooks = $('.bk-dsp .card').filter(function () {
      var bookTitle = $(this).find('.card-title').text().toLowerCase();
      var bookAuthors = $(this).find('.card-text').text().toLowerCase();

      if (searchBy === 'author') {
        return bookAuthors.includes(query);
      } else {
        return bookTitle.includes(query);
      }
    });

    // Show or hide the filtered books
    $('.bk-dsp .card').hide();
    filteredBooks.show();

    // Clear the search results and show all books when the search input is empty
    if (query.trim() === '') {
      $('.bk-dsp .card').show();
    }
  });

  // MODAL
  // Function to fill the modal with book details
  function showBookModal(title, authors, description, coverImage) {
    $('#bookModalLabel').text(title);
    $('#modalTitle').text(title);
    $('#modalAuthors').text(authors);
    $('#modalDescription').text(description);
    $('#modalCoverImage').attr('src', coverImage);

    // Show the modal
    $('#bookModal').modal('show');

    // Add click event to the "Add to Cart" button in the modal
    $('#addToCartButton').click(function () {
      addToCart(title, authors, coverImage); // Call the function to add the book to the cart
    });
  }

  // Attach click event to each book card
  $('.book-details').click(function (event) {
    // Check if the clicked element is the like button or the star rating button
    if ($(event.target).hasClass('like') || $(event.target).hasClass('far')) {
      return;
    }

    // Prevent triggering the modal for other elements like the star icons or the book card itself
    if ($(event.target).hasClass('fa-solid') || $(event.target).hasClass('bk-stars')) {
      return;
    }

    var title = $(this).data('title');
    var authors = $(this).data('authors');
    var description = $(this).data('description');
    var coverImage = $(this).data('cover');

    // Call the function to show the modal with book details
    showBookModal(title, authors, description, coverImage);
  });

});

// Event listener for "Add to Cart" button in the modal
$('#addToCartButton').click(function () {
  // Implement the logic to add the book to the cart here

  var cartItemCount = parseInt($('.cart-item-count').text());
  $('.cart-item-count').text(cartItemCount + 1);
  // For demonstration purposes, let's assume the book is successfully added to the cart
  // and redirect the user to the cart page after a short delay (2 seconds)

  // Wait for 2 seconds before redirecting to the cart page
  setTimeout(function () {
    window.location.href = '/cart'; // Replace '/cart' with the URL of your cart page
  }, 200); // 200 milliseconds = 0.2 seconds
});

// JavaScript function to add book to cart
function addToCart(title, authors, coverImage) {
  // ... (existing code)
  $('#bookModalLabel').text(title);
  $('#modalTitle').text(title);
  $('#modalAuthors').text(authors);
  $('#modalDescription').text(description);
  $('#modalCoverImage').attr('src', coverImage);

  // Show the modal
  $('#bookModal').modal('show');

  // Add click event to the "Add to Cart" button in the modal
  $('#addToCartButton').click(function () {
    addToCart(title, authors, coverImage, description); // Pass the description to the addToCart function
  });

  fetch('/add_to_cart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bookData),
  })
  .then((response) => {
    if (response.ok) {
      // Redirect the user to the '/cart' page after adding the book to the cart
      window.location.href = '/cart';
    } else {
      console.error('Error adding book to cart:', response.statusText);
    }
  })
  .catch(error => {
    console.error('Error adding book to cart:', error);
  });
}

