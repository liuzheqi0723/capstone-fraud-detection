import { Card } from 'antd';
import React from "react";
import './serverCard.css';
import { SmileTwoTone, FrownTwoTone, MehTwoTone } from '@ant-design/icons';
class SysCard extends React.Component {
    constructor() {
        super();
        this.state = {
            serverUpHr: "--",
            serverUpMin: "--",
            serverUpSec: "--",
            serverStatus: <MehTwoTone twoToneColor='#f5ad42' style={{ fontSize: '32px' }}/>
        }
        this.check = this.check.bind(this);
    }

    componentDidMount(){
        setInterval(this.check, 5000);
        fetch("http://localhost:5000/server_time")
        .then(res => res.json()
        ).then((result) => {
            this.setState({runtime: result.server_time})
            setInterval(()=>{
                this.state.runtime += 1;
                this.updateTime();
            },1000)
        })
    }
    updateTime(){
        let hrs = Math.floor(this.state.runtime / 3600);
            let mins = Math.floor(this.state.runtime % 3600 / 60);
            let secs = Math.floor(this.state.runtime % 3600 % 60);
            this.setState({
                serverUpHr:hrs,
                serverUpMin:mins,
                serverUpSec:secs
            })
    }
    

    check() {
        fetch("http://localhost:5000/ping")
        .then(res => res.json()
        ).then((result) =>{
            if(result.msg === "pong"){
                this.setState(
                    {serverStatus: <SmileTwoTone twoToneColor='#34eb34' style={{ fontSize: '32px' }}/>}
                )
            }
        console.log(this.state);
        }).catch(err => {
            this.setState(
                {serverStatus: <FrownTwoTone twoToneColor='#eb3d34' style={{ fontSize: '32px' }}/>}
            )
        })
    }

    tick(){

    }

    render() {
        return (
            <Card title="Server Status Stats" style={{ height: "100%" }}>
                <table className='CardTable'>
                    <tr>
                        <th>Server up time:</th>
                        <td>{this.state.serverUpHr}H:
                        {this.state.serverUpMin}M:
                        {this.state.serverUpSec}S</td>
                    </tr>
                    <tr>
                        <th>Server Status:</th>
                        <td>{this.state.serverStatus}</td>
                    </tr>
                </table>
            </Card>
        )
    }

}

export default SysCard;