import React from "react"
import Layout from "../components/layout"
import "../styles/custom.css"

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      timeout: null,
      rooms: {},
    }
    this.get_rooms()
    setInterval(() => this.get_rooms(), 5000)
  }

  get_rooms() {
    fetch("http://127.0.0.1:5000/get_room_detial_list", {
      method: "GET",
    })
      .then(response => {
        response.json().then(data => {
          console.log(data)
          this.setState({
            rooms: data.rooms,
          })
        })
      })
      .catch(error => console.log(error))
  }

  isEmptyObject(obj) {
    for (var _ in obj) {
      return false
    }
    return true
  }

  render() {
    let message = ""
    if (this.isEmptyObject(this.state.rooms)) {
      message = "No room is being used now."
    }
    return (
      <Layout>
        <div className="App">
          <div>
            {message}
            <br />
          </div>

          {Object.keys(this.state.rooms).map(room_id => (
            <div>
              <br />
              <hr />
              <div>Room #{room_id}</div>
              <br />
              <hr />
              <div>
                {this.state.rooms[room_id].map(detial => (
                  <div>
                    <p>服务开始时间: {detial[1]}</p>
                    <p>
                      起始温度：{detial[3]} 目标温度：{detial[4]}
                    </p>
                    <p>模式：{detial[5]}</p>
                    <p>风速：{detial[6]}</p>
                    <p>费率：{detial[7]}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div>
          <br />
          <a href="/">Back</a>
        </div>
      </Layout>
    )
  }
}

export default App
