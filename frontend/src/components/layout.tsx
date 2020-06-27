import React from "react"
import Helmet from "react-helmet"
import { useStaticQuery, Link, graphql } from "gatsby"

export default function Layout({ children }) {
  const data = useStaticQuery(
    graphql`
      query {
        site {
          siteMetadata {
            title
            siteURL
          }
        }
      }
    `
  )
  return (
    <div className="application">
      <Helmet>
        <meta charSet="utf-8" />
        <title>{data.site.siteMetadata.title}</title>
        <link rel="canonical" href={data.site.siteMetadata.siteURL} />
      </Helmet>
      <div
        className="main"
        style={{ margin: `3rem auto`, maxWidth: 650, padding: `0 1rem` }}
      >
        <header style={{ marginBottom: `1.5rem` }}>
          <Link to="/" style={{ textShadow: `none`, backgroundImage: `none` }}>
            <h3 style={{ display: `inline` }}>
              {data.site.siteMetadata.title}
            </h3>
          </Link>
        </header>
        <div className="panel">{children}</div>
        <footer>
          Powered by <a href="https://github.com/JmPotato/DCTCS">DCTCS</a> & Go
          to <a href="/admin">Admin</a>
        </footer>
      </div>
    </div>
  )
}
