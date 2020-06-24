import Typography from "typography"
import funstonTheme from "typography-theme-funston"

funstonTheme.headerFontFamily = ["Aam Patua One", "sans-serif"]
funstonTheme.bodyFontFamily = ["Aam Cabin Condensed", "georgia", "sans-serif"]

const typography = new Typography(funstonTheme)

export default typography
export const rhythm = typography.rhythm
