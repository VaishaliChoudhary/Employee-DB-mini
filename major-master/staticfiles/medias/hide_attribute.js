document.addEventListener('DOMContentLoaded', function(){
    console.log("hello");
    function toggleCity(value) {
      const cityWrapper = document.querySelector('.field-cet');
      console.log(value);
      if (value === '1') {
          cityWrapper.style.display = 'none';
      } else {
          cityWrapper.style.display = 'block';
      }
    }
    
    const formatSelect = document.querySelector('select#id_semester');
    if (formatSelect) {
        toggleCity(formatSelect.value);
   
        formatSelect.addEventListener('click', function(){
            toggleCity(this.value);
        })    
    }
  
  })