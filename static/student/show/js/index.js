// 立即执行函数，防止变量污染 (function() {})();



// main head
(function () {
  $.ajax({
    url: '/api/completion_statistics',  // 使用我们新创建的API接口
    method: 'GET',
    dataType: 'json',
    success: function(data) {
        // 更新完成和未完成的数据显示
        $('#data1').text(data.completed);
        $('#data2').text(data.notCompleted);
    },
    error: function(xhr, status, error) {
        console.error('获取数据时出错:', error);
        // 处理错误，显示错误提示
        $('#data1').text('获取失败');
        $('#data2').text('获取失败');
    }
  });
})();





// 各院系在校生参测率
// main body
(function () {
  var myChart = echarts.init(document.querySelector('.map .chart'));

  // 定义颜色数组
  var colors = ['#3282b8', '#66bb6a', '#ff9800', '#9c27b0', '#e57373', '#00bcd4', '#8bc34a', '#f44336', '#03a9f4', '#9e9e9e', '#ff5722', '#607d8b', '#4caf50', '#f06292', '#2196f3', '#795548', '#ffc107', '#3f51b5', '#009688', '#cddc39', '#f57c00', '#81d4fa', '#f50057', '#673ab7', '#455a64', '#7e57c2', '#00e676', '#90a4ae', '#ff8a80', '#0091ea', '#82b1ff', '#4db6ac', '#d1c4e9', '#00b0ff', '#b2dfdb', '#000000'];

  // 从接口获取数据
  function fetchData() {
    $.ajax({
      url: '/api/college_participation_rate',
      method: 'GET',
      dataType: 'json',
      success: function(response) {
        var data = response.data;
        
        var option = {
          title: {
            text: '各院系在校生参测率',
            left: '36%',
            textStyle: {
              color: "#FFFFFF"
            },
          },
          xAxis: {
            type: 'value',
            axisLabel: {
              textStyle: {
                color: '#FFFFFF'
              }
            },
          },
          grid: {
            top: 48,
            left: 155,
            right: 50,
            bottom: 50,
          },
          yAxis: {
            type: 'category',
            data: data.map(item => item.name),
            axisLabel: {
              textStyle: {
                color: '#FFFFFF'
              }
            },
          },
          series: [{
            name: '参测率',
            type: 'bar',
            data: data.map(item => item.value),
            label: {
              show: true,
              position: 'insideRight',
              formatter: '{c}%',  // 添加百分号
              color: '#FFFFFF'
            },
            itemStyle: {
              color: function(params) {
                return colors[params.dataIndex % colors.length];  // 使用取模运算确保不会超出颜色数组范围
              }
            }
          }]
        };

        myChart.setOption(option);
      },
      error: function(xhr, status, error) {
        console.error('获取数据失败:', error);
      }
    });
  }

  // 初次加载数据
  fetchData();

  // 让图表随屏幕自适应
  window.addEventListener('resize', function() {
    myChart.resize();
  });
})();




// 柱状图1
// 各年级成绩分布对比
// 11
(function () {
  var myChart = echarts.init(document.querySelector('.bar .chart'));
  
  // 定义一个函数从接口获取数据
  function fetchData() {
    $.ajax({
      url: '/api/grade_score_distribution',
      method: 'GET',
      dataType: 'json',
      success: function (response) {
        var data = response.data;
        var option = {
          color: ['#FF0000', '#ffff00', '#00FA9A', '#0096ff'],
          legend: {
            data: ['优秀', '良好', '及格', '不及格'],
            textStyle: {
              color: '#ffffff'
            },
            left: 'center',
            top: '8%',
            padding: [5, 10]
          },
          xAxis: {
            type: 'value',
            name: '',
            textStyle: {
              color: '#ffffff'
            }
          },
          yAxis: {
            type: 'category',
            data: ['大一', '大二', '大三', '大四'],
            textStyle: {
              color: '#ffffff'
            }
          },
          series: [
            {
              name: '优秀',
              type: 'bar',
              data: data['优秀'],
              stack: '总量'
            },
            {
              name: '良好',
              type: 'bar',
              data: data['良好'],
              stack: '总量'
            },
            {
              name: '及格',
              type: 'bar',
              data: data['及格'],
              stack: '总量'
            },
            {
              name: '不及格',
              type: 'bar',
              data: data['不及格'],
              stack: '总量'
            }
          ],
          barWidth: 8,
          textStyle: {
            color: '#ffffff'
          }
        };

        myChart.setOption(option);
      },
      error: function (xhr, status, error) {
        console.error('获取数据失败:', error);
      }
    });
  }

  // 初次加载数据
  fetchData();

  // 让图表随屏幕自适应
  window.addEventListener('resize', function () {
    myChart.resize();
  });
})();





// 柱状图2
//不同群体体测平均成绩
// 12

(function () {
  // 1.实例化对象
  var myChart = echarts.init(document.querySelector(".bar2 .chart"));
  // 2.指定配置项和数据
  var option = {
    color: ['#2f89cf'],
    // 提示框组件
    tooltip: {
      trigger: 'axis',
      axisPointer: { // 坐标轴指示器，坐标轴触发有效
        type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
      }
    },
    // 修改图表位置大小
    grid: {
      left: '0%',
      top: '10px',
      right: '0%',
      bottom: '4%',
      containLabel: true
    },
    // x轴相关配置
    xAxis: [{
      type: 'category',
      data: ["旅游行业", "教育培训", "游戏行业", "医疗行业", "电商行业", "社交行业", "金融行业"],
      axisTick: {
        alignWithLabel: true
      },
      // 修改刻度标签，相关样式
      axisLabel: {
        color: "rgba(255,255,255,0.8)",
        fontSize: 10
      },
      // x轴样式不显示
      axisLine: {
        show: false
      }
    }],
    // y轴相关配置
    yAxis: [{
      type: 'value',
      // 修改刻度标签，相关样式
      axisLabel: {
        color: "rgba(255,255,255,0.6)",
        fontSize: 12
      },
      // y轴样式修改
      axisLine: {
        lineStyle: {
          color: "rgba(255,255,255,0.6)",
          width: 2
        }
      },
      // y轴分割线的颜色
      splitLine: {
        lineStyle: {
          color: "rgba(255,255,255,0.1)"
        }
      }
    }],
    // 系列列表配置
    series: [{
      name: '直接访问',
      type: 'bar',
      barWidth: '35%',
      // ajax传动态数据
      data: [200, 300, 300, 900, 1500, 1200, 600],
      itemStyle: {
        // 修改柱子圆角
        barBorderRadius: 5
      }
    }]
  };
  // 3.把配置项给实例对象
  myChart.setOption(option);

  // 4.让图表随屏幕自适应
  window.addEventListener('resize', function () {
    myChart.resize();
  })
})();




// 折线图1
// 各年级平均BMI
// 21
(function () {
  var myChart = echarts.init(document.querySelector(".line .chart"));

  // 定义一个函数从接口获取数据
  function fetchData() {
    $.ajax({
      url: '/api/average_bmi_data', // 替换为你的实际接口地址
      method: 'GET',
      dataType: 'json',
      success: function (response) {
        // 假设返回的数据结构为 { data: { bmi: [...], weight: [...], height: [...] } }
        var yearData = response.data;
        var option = {
          // 修改两条线的颜色
          color: ['#00f2f1', '#ed3f35', '#FFA500'],
          tooltip: {
            trigger: 'axis'
          },
          // 图例组件
          legend: {
            textStyle: {
              color: '#4c9bfd'
            },
            right: '10%',
          },
          grid: {
            top: "20%",
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true,
            show: true,
            borderColor: '#012f4a'
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['大一', '大二', '大三', '大四'],
            axisTick: {
              show: false
            },
            axisLabel: {
              color: "#4c9bfb"
            },
            axisLine: {
              show: false
            }
          },
          yAxis: {
            type: 'value',
            axisTick: {
              show: false
            },
            axisLabel: {
              color: "#4c9bfb"
            },
            axisLine: {
              show: false
            },
            splitLine: {
              lineStyle: {
                color: "#012f4a"
              }
            }
          },
          series: [{
            type: 'line',
            smooth: true,
            name: '平均BMI',
            data: yearData.bmi
          },
          {
            type: 'line',
            smooth: true,
            name: '平均体重',
            data: yearData.weight
          },
          {
            type: 'line',
            smooth: true,
            name: '平均身高',
            data: yearData.height
          }
          ]
        };

        myChart.setOption(option);
      },
      error: function (xhr, status, error) {
        console.error('获取数据失败:', error);
      }
    });
  }

  // 初次加载数据
  fetchData();

  // 让图表随屏幕自适应
  window.addEventListener('resize', function () {
    myChart.resize();
  });
})();






// 折线图2
// 体测成绩时间序列趋势
// 22

(function () {
  var myChart = echarts.init(document.querySelector('.line2 .chart'));

  var option = {
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      top: "0%",
      textStyle: {
        color: "rgba(255,255,255,.5)",
        fontSize: "12"
      }
    },
    grid: {
      top: '30',
      left: '10',
      right: '30',
      bottom: '10',
      containLabel: true
    },
    xAxis: [{
      type: 'category',
      boundaryGap: false,
      // 文本颜色为rgba(255,255,255,.6)  文字大小为 12
      axisLabel: {
        textStyle: {
          color: "rgba(255,255,255,.6)",
          fontSize: 12
        }
      },
      // x轴线的颜色为   rgba(255,255,255,.2)
      axisLine: {
        lineStyle: {
          color: "rgba(255,255,255,.2)"
        }
      },
      data: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "26", "28", "29", "30"]
    }],
    yAxis: [{
      type: 'value',
      axisTick: {
        // 不显示刻度线
        show: false
      },
      axisLine: {
        lineStyle: {
          color: "rgba(255,255,255,.1)"
        }
      },
      axisLabel: {
        textStyle: {
          color: "rgba(255,255,255,.6)",
          fontSize: 12
        }
      },
      // 修改分割线的颜色
      splitLine: {
        lineStyle: {
          color: "rgba(255,255,255,.1)"
        }
      }
    }],
    series: [{
      name: '邮件营销',
      type: 'line',
      smooth: true, // 圆滑的线
      // 单独修改当前线条的样式
      lineStyle: {
        color: "#0184d5",
        width: 2
      },
      // 填充区域渐变透明颜色
      areaStyle: {
        color: new echarts.graphic.LinearGradient(
          0,
          0,
          0,
          1,
          [{
            offset: 0,
            color: "rgba(1, 132, 213, 0.4)" // 渐变色的起始颜色
          },
          {
            offset: 0.8,
            color: "rgba(1, 132, 213, 0.1)" // 渐变线的结束颜色
          }
          ],
          false
        ),
        shadowColor: "rgba(0, 0, 0, 0.1)"
      },
      // 拐点设置为小圆点
      symbol: 'circle',
      // 设置拐点大小
      symbolSize: 5,
      // 开始不显示拐点， 鼠标经过显示
      showSymbol: false,
      // 设置拐点颜色以及边框
      itemStyle: {
        color: "#0184d5",
        borderColor: "rgba(221, 220, 107, .1)",
        borderWidth: 12
      },
      data: [30, 40, 30, 40, 30, 40, 30, 60, 20, 40, 30, 40, 30, 40, 30, 40, 30, 60, 20, 40, 30, 40, 30, 40, 30, 40, 20, 60, 50, 40]
    },
    {
      name: "转发量",
      type: "line",
      smooth: true,
      lineStyle: {
        normal: {
          color: "#00d887",
          width: 2
        }
      },
      areaStyle: {
        normal: {
          color: new echarts.graphic.LinearGradient(
            0,
            0,
            0,
            1,
            [{
              offset: 0,
              color: "rgba(0, 216, 135, 0.4)"
            },
            {
              offset: 0.8,
              color: "rgba(0, 216, 135, 0.1)"
            }
            ],
            false
          ),
          shadowColor: "rgba(0, 0, 0, 0.1)"
        }
      },
      // 设置拐点 小圆点
      symbol: "circle",
      // 拐点大小
      symbolSize: 5,
      // 设置拐点颜色以及边框
      itemStyle: {
        color: "#00d887",
        borderColor: "rgba(221, 220, 107, .1)",
        borderWidth: 12
      },
      // 开始不显示拐点， 鼠标经过显示
      showSymbol: false,
      data: [130, 10, 20, 40, 30, 40, 80, 60, 20, 40, 90, 40, 20, 140, 30, 40, 130, 20, 20, 40, 80, 70, 30, 40, 30, 120, 20, 99, 50, 20]
    }
    ]
  };

  myChart.setOption(option);

  window.addEventListener('resize', function () {
    myChart.resize();
  })
})();



// 饼形图1
//体测数据异常值占比
// 31
(function () {
  // 定义一个异步函数来获取数据
  $.ajax({
    url: 'http://127.0.0.1:8000/api/distribution_of_actual_test_scores', // 替换为你的数据接口
    type: 'GET', // 请求类型
    dataType: 'json', // 期望的返回数据类型
    success: function (data) {
      final_data = data.data; // 将返回的数据存储到 final_data 变量中
      var myChart = echarts.init(document.querySelector(".pie .chart"));
      var option = {
        color: ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6"],
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          // 垂直居中,默认水平居中
          // orient: 'vertical',

          bottom: 0,
          left: 10,
          // 小图标的宽度和高度
          itemWidth: 10,
          itemHeight: 10,
          // 修改图例组件的文字为 12px
          textStyle: {
            color: "rgba(255,255,255,.5)",
            fontSize: "10"
          }
        },
        series: [{
          name: '成绩',
          type: 'pie',
          // 设置饼形图在容器中的位置
          center: ["50%", "42%"],
          // 修改饼形图大小，第一个为内圆半径，第二个为外圆半径
          radius: ['40%', '60%'],
          avoidLabelOverlap: false,
          // 图形上的文字
          label: {
            show: false,
            position: 'center'
          },
          // 链接文字和图形的线
          labelLine: {
            show: false
          },
          data: final_data
        }]
      };

      myChart.setOption(option);
      window.addEventListener('resize', function () {
        myChart.resize();
      })
    }
  });
})();





// 饼形图2
// 体测数据异常值占比
// 33
(function () {
  var myChart = echarts.init(document.querySelector('.pie2 .chart'));
  var option = {
    color: ['#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff'],
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    legend: {
      bottom: 0,
      itemWidth: 10,
      itemHeight: 10,
      textStyle: {
        color: "rgba(255,255,255,.5)",
        fontSize: 10
      }
    },
    series: [{
      name: '地区分布',
      type: 'pie',
      radius: ["10%", "60%"],
      center: ['50%', '40%'],
      // 半径模式  area面积模式
      roseType: 'radius',
      // 图形的文字标签
      label: {
        fontsize: 10
      },
      // 引导线调整
      labelLine: {
        // 连接扇形图线长(斜线)
        length: 6,
        // 连接文字线长(横线)
        length2: 8
      },
      data: [{
        value: 26,
        name: '北京'
      },
      {
        value: 24,
        name: '山东'
      },
      {
        value: 25,
        name: '河北'
      },
      {
        value: 20,
        name: '江苏'
      },
      {
        value: 25,
        name: '浙江'
      },
      {
        value: 30,
        name: '四川'
      },
      {
        value: 42,
        name: '湖北'
      }
      ]
    }]
  };

  myChart.setOption(option);
  window.addEventListener('resize', function () {
    myChart.resize();
  })
})();



