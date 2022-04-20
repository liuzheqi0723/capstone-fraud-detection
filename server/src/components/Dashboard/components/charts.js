import React from "react";
import ApexCharts from "react-apexcharts";
// const series = [{
//   name: 'Your Activity',
//   type: 'column',
//   data: [350, 275, 375, 375, 300, 225, 275]
// }, {
//   name: 'Your Goal',
//   type: 'line',
//   data: [400, 350, 450, 400, 350, 300, 350]

// }];

 class ApexActivityChart extends React.Component{
  constructor(){
    super();
    this.state = {
      options : {
        colors: ["#FFCA41", "#43BC13"],
        chart: {
          height: 350,
          stacked: true,
          type: "bar",
          toolbar: {
            show: false,
          },
          animations: {
            enabled: false, //no animations
          }
        },
        labels: ['h', 'g', 'q', 'q', 'o'],
        stroke: {
          curve: "straight",
          width: [0, 1]
        },
        dataLabels: {
          enabled: true,
          enabledOnSeries: [1],
          style: {
            fontSize: '10px',
            fontWeight: 500,
          },
          background: {
            borderWidth: 0,
          },
        },
        legend: {
          position: "top",
          floating: true,
        },
        xaxis: {
          type: 'category',
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          },
          labels: {
            show: true,
            style: {
              colors: "#6B859E",
            },
          },
        },
        yaxis: {
          show: false,
        },
        fill: {
          type: "solid",
          opacity: 1,
        },
        plotOptions: {
          bar: {
            borderRadius: 10,
          }
        },
        grid: {
          show: false,
        }
      },
      series: []
    }
  }

  componentDidMount(){
    fetch("http://localhost:5000/search_model")
    .then(
        res => res.json()
    ).then(
        (result) => {
            var prediction = {
                name: 'Made prediction',
                data: {}
            }
            var fraud = {
                name: 'Fraud predicted',
                data: {}
            }
            for(var model_data of result.result){
                if(model_data[2] === 1){
                  fraud.data[model_data[1]] = model_data[0]
                }else{
                  prediction.data[model_data[1]] = model_data[0]
                }
            }

            prediction.data = Object.keys(prediction.data).sort().reduce(
              (obj, key) => { 
                obj[key] = prediction.data[key]; 
                return obj;
              }, 
              {}
            );
            fraud.data = Object.keys(fraud.data).sort().reduce(
              (obj, key) => { 
                obj[key] = fraud.data[key]; 
                return obj;
              }, 
              {}
            );
            var categories = Object.keys(prediction.data);
            prediction.data = Object.values(prediction.data);
            fraud.data = Object.values(fraud.data);

            var new_options = {...this.state};
            new_options.labels = categories;
            this.setState({
              options: new_options,
              series : [prediction, fraud],
            })
            console.log(this.state);
        }
    )
  }
  
  render(){
    return (
      <ApexCharts
        type="bar"
        options={this.state.options}
        series={this.state.series}
        width={"100%"}
      />
    )
  }
  
}
export default ApexActivityChart;