import React from "react"
import Layout from "../components/layout"
import "../styles/custom.css"

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      room_id: null,
      is_checked_in: false,
      is_checked_out: false,
      cur_temp: 25.0,
      cur_speed: "mid",
      target_temp: 25.0,
      target_speed: "mid",
      elctr_usage: 0,
      fee: 0,
      AC_state: 0, // 1表示空调处于开启状态，0表示关闭状态
      timeout: null,
    }
  }

  heart_beat() {
    fetch(
      "http://127.0.0.1:5000/status_heartbeat?room_id=" + this.state.room_id,
      {
        method: "GET",
      }
    )
      .then(response => {
        response.json().then(data => {
          this.setState({
            elctr_usage: data.electrical_usage,
            fee: data.fee,
            cur_speed: data.speed,
            cur_temp: data.temperature,
          })
        })
      })
      .catch(error => console.log(error))
  }

  check_in() {
    fetch("http://127.0.0.1:5000/check_in", {
      method: "POST",
    })
      .then(response => {
        response.json().then(data => {
          this.setState({
            is_checked_in: true,
            room_id: data.room_id,
          })
        })
      })
      .catch(error => console.log(error))
  }

  check_out() {
    const form_data = new URLSearchParams()
    form_data.append("room_id", this.state.room_id)
    fetch("http://127.0.0.1:5000/check_out", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: form_data,
    })
      .then(response => {
        response.json().then(_ => {
          this.setState({
            is_checked_in: false,
            is_checked_out: true,
          })
        })
      })
      .catch(error => console.log(error))
  }

  turn_off() {
    let state = 0
    this.setState({
      AC_state: state,
    })
    clearInterval(this.state.timeout)
  }

  turn_on() {
    let state = 1
    let timeout = setInterval(() => this.heart_beat(), 5000)
    this.setState({
      timeout: timeout,
      AC_state: state,
    })
  }

  adj_tempr(temp) {
    this.setState({
      target_temp: Number(temp).toFixed(1),
    })
    const form_data = new URLSearchParams()
    form_data.append("room_id", this.state.room_id)
    form_data.append("cur_temp", this.state.cur_temp)
    form_data.append("cur_speed", this.state.cur_speed)
    form_data.append("target_temp", Number(temp).toFixed(1))
    fetch("http://127.0.0.1:5000/adjust_temperature", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: form_data,
    })
      .then(response => {
        response.json().then(data => {
          console.log(data)
        })
      })
      .catch(error => console.log(error))
  }

  adj_speed() {
    this.setState({
      cur_speed: document.getElementById("speed").value,
    })
    const form_data = new URLSearchParams()
    form_data.append("room_id", this.state.room_id)
    form_data.append("cur_temp", this.state.cur_temp)
    form_data.append("cur_speed", document.getElementById("speed").value)
    form_data.append("target_speed", document.getElementById("speed").value)
    fetch("http://127.0.0.1:5000/adjust_wind", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: form_data,
    })
      .then(response => {
        response.json().then(data => {
          console.log(data)
        })
      })
      .catch(error => console.log(error))
  }

  render() {
    return (
      <Layout>
        <div className="App">
          {this.state.is_checked_in ? (
            <div>
              <h5>Room:{this.state.room_id}</h5>
              {this.state.AC_state ? (
                <div>
                  Target temperature: {this.state.target_temp} ℃
                  <button
                    className="btn"
                    onClick={() =>
                      this.adj_tempr(Number(this.state.target_temp) + 1)
                    }
                  >
                    +
                  </button>
                  <button
                    onClick={() =>
                      this.adj_tempr(Number(this.state.target_temp) - 1)
                    }
                  >
                    -
                  </button>
                  <br />
                  Target speed:
                  <select name="speed" id="speed">
                    <option value="mid">Mid</option>
                    <option value="low">Low</option>
                    <option value="high">High</option>
                  </select>
                  <button className="btn" onClick={() => this.adj_speed()}>
                    OK
                  </button>
                  <hr />
                  <h5>Details:</h5>
                  <p>Electrical usage : {this.state.elctr_usage} kwh</p>
                  <p>Fee : {this.state.fee} RMB</p>
                  <p>Speed : {this.state.cur_speed}</p>
                  <p>Temperature : {this.state.cur_temp} ℃</p>
                  <hr />
                  <button onClick={() => this.turn_off()}>Off</button>
                </div>
              ) : (
                <div>
                  <br />
                  <br />
                  <p>
                    The AC is off now, please click the button to turn on the AC
                    and have a nice day :)
                  </p>
                  <br />
                  <br />
                  <hr />
                  <button onClick={() => this.turn_on()}>On</button>
                </div>
              )}
              <br />
              <br />
              <button onClick={() => this.check_out()}>Check out</button>
            </div>
          ) : (
            <div>
              {this.state.is_checked_out ? (
                <div>
                  <p>This is the checked out page. To be continued...</p>
                </div>
              ) : (
                <div>
                  <br />
                  <br />
                  <h4>Welcome!</h4>
                  <hr />
                  <p>
                    To use the DCTCS, please check in to get your room and turn
                    on the AC. If you are done with the AC, please make sure it
                    is off and you can check your bill after checkout.
                  </p>
                  <p>
                    <strong>Have a nice day!</strong>
                  </p>
                  <br />
                  <button onClick={() => this.check_in()}>Check in</button>
                </div>
              )}
            </div>
          )}
        </div>
      </Layout>
    )
  }
}

export default App
