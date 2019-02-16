// Modified version of https://codepen.io/fancyapps/full/pxovaa
// Template for custom "info" button
$.fancybox.defaults.btnTpl.info = '<button data-fancybox-info class="fancybox-button fancybox-button--info" title="Show image information">\
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">\
    <path d="M3.968,12.061C1.775,12.061,0,13.835,0,16.027c0,2.192,1.773,3.967,3.968,3.967c2.189,0,3.966-1.772,3.966-3.967 C7.934,13.835,6.157,12.061,3.968,12.061z M16.233,12.061c-2.188,0-3.968,1.773-3.968,3.965c0,2.192,1.778,3.967,3.968,3.967 s3.97-1.772,3.97-3.967C20.201,13.835,18.423,12.061,16.233,12.061z M28.09,12.061c-2.192,0-3.969,1.774-3.969,3.967 c0,2.19,1.774,3.965,3.969,3.965c2.188,0,3.965-1.772,3.965-3.965S30.278,12.061,28.09,12.061z"/>\
  </svg>\
  </button>';

// Initialize fancybox with custom settings
$('[data-fancybox="gallery"]').fancybox({
  preventCaptionOverlap: false,
  infobar: false,

  // Disable idle
  idleTime: 0,

  // Display only these two buttons
  buttons: [
    'info', 'close'
  ],

  // Custom caption content
  caption: function(instance, obj) {
    return $(this).find('.image-info').html();
  },

  onInit: function(instance) {
    // Toggle caption on tap
    instance.$refs.container.on('touchstart', '[data-fancybox-info]', function(e) {
      e.stopPropagation();
      e.preventDefault();

      instance.$refs.container.toggleClass('fancybox-vertical-caption');
    });

    // Display caption on button hover
    instance.$refs.container.on('mouseenter', '[data-fancybox-info]', function(e) {
      instance.$refs.container.addClass('fancybox-vertical-caption');

      // Hide caption when mouse leaves caption area
      instance.$refs.caption.one('mouseleave', function(e) {
        instance.$refs.container.removeClass('fancybox-vertical-caption');
      });
    });
  }
});
