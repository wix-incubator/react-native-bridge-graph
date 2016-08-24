import _ from 'lodash';
import moment from 'moment';
import Message from './src/BridgeParsing';

const NATIVE_TO_JS = "N->JS"
const JS_TO_NATIVE = "JS->N"

function generateGraph(data, element) {
  Plotly.plot(element, data, {
    barmode: 'stack'
  });
}

function buildBarTraceByTimesDict(timesDict, name) {
  const dates = _.keys(timesDict)
  const counts = _.map(dates, (time) => timesDict[time].length)

  const data = {
    x: _.map(dates, (date) => moment(date).format("YYYY-MM-DD hh:mm:ss")), // Formatting to Plot.ly date format
    y: counts,
    type: 'bar',
    name
  }

  return data
}

function buildBarTraceByBridgeType(messages, bridgeType) {
  const myDict = Message.dictOfMessagesByTime(Message.filterByBridgeType(messages, bridgeType));
  return buildBarTraceByTimesDict(myDict, bridgeType);
}

function buildDataByCalledFunctions(messages) {
  const dictByCalledFuncs = Message.dictOfMessagesByCalledFunc(messages);
  const calledFuncs = _.keys(dictByCalledFuncs);

  const data = [];

  calledFuncs.forEach((calledFunc) => {
    const timesDict = Message.dictOfMessagesByTime(dictByCalledFuncs[calledFunc]);
    data.push(buildBarTraceByTimesDict(timesDict, calledFunc));
  });

  return data;
}

function main() {
  var log = require('fs').readFileSync('./log.txt', 'utf8');
  const messages = Message.messagesByLog(log);
  generateGraph(buildDataByCalledFunctions(Message.filterByBridgeType(messages, JS_TO_NATIVE)), 'js-to-native');
  generateGraph(buildDataByCalledFunctions(Message.filterByBridgeType(messages, NATIVE_TO_JS)), 'native-to-js');
}

main();
