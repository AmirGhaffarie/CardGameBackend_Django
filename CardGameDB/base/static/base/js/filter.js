window.addEventListener("load", function() {
(function($) {
  $(document).ready(function() {

    // Listen for changes to the field
    $("select[name='group']").change(function() {
      let newValue = $(this).val();
    });
  });
})(django.jQuery); })