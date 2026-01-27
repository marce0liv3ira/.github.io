module.exports = {
  extends: "stylelint-config-standard-scss",
  rules: {
    // Disallow import-notation since:
    // - If url is not added importing fonts, fonts are not loaded
    // - If url is added importing local bootstrap scss, we get an error
    "import-notation": null,
    // "context" notation does not work with LibSass
    // TODO: make Hugo use DartSass instead of LibSass
    "media-feature-range-notation": "prefix",
    // Do not force CSS order since it is not working properly
    "no-descending-specificity": null,
    // Allow using extend without placeholders since we extend bootstrap classes
    "scss/at-extend-no-missing-placeholder": null,
    // color.adjust does not work with LibSass
    // See: https://sass-lang.com/documentation/modules/color/
    // Hence, we must use lighten function
    // TODO: make Hugo use DartSass
    "scss/no-global-function-names": null,
  },
};
