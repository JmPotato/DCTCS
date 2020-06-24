/**
 * Configure your Gatsby site with this file.
 *
 * See: https://www.gatsbyjs.org/docs/gatsby-config/
 */

module.exports = {
  /* Your site config here */
  siteMetadata: {
    title: `DCTCS`,
    siteURL: `http://localhost:8000/`,
  },
  plugins: [
    {
      resolve: "gatsby-plugin-manifest",
      options: {
        name: "DCTCS",
        short_name: "DCTCS",
        start_url: "/",
        icon: "src/images/icon.png",
      },
    },
    `gatsby-plugin-react-helmet`,
    {
      resolve: `gatsby-plugin-typography`,
      options: {
        pathToConfigModule: `src/utils/typography`,
        omitGoogleFont: true,
      },
    },
  ],
}
