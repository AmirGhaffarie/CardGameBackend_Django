window.addEventListener("load", function() {
(function($) {
  $(document).ready(function() {
    // Listen for changes to the field
    $("id_group").on('change', function() {
      // Perform your logic here
      let newValue = $(this).val();
      // Access the new field value and perform any desired actions
      console.log('Field value changed to: ' + newValue);
    });
  });
})(django.jQuery); })