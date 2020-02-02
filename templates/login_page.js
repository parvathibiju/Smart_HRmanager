import React from "react";

class FormElementCombined extends React.Component {

    constructor(props) {
        super(props);
        this.state = { value1: '', value2: '',};
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        if (event.target.name === "username") {
            this.setState({ value1: event.target.value })
        }
        else if (event.target.name === "password") {
            this.setState({ value2: event.target.value })
        }

        
    }

    handleSubmit(event) {
       // alert('A detail as submitted: ' + this.state.value1 + " " + this.state.value2);
        if (this.state.value1 === '' ||this.state.value2 === ''  )
            event.preventDefault();
    }
    render() {
        return (
            <div>
                <form action="https://zu8ucbt3qd.execute-api.us-east-1.amazonaws.com/sahithya123" onSubmit={this.handleSubmit} name="myform" method="POST">
                    LOGIN : <input type="text" value={this.state.value1} name="username" onChange={this.handleChange} /> <br/><br/>

 PASSWORD: <input type="text" value={this.state.value2} name="password" onChange={this.handleChange} /> <br/><br/>



                  
                    <input type="submit" value="submit" />
                </form>
            </div>
        )
    }
}
export default FormElementCombined
