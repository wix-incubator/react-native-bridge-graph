import _ from 'lodash';
import moment from 'moment';

class Message {
  constructor(time, pid, tid, tag, bridgeType, content, calledFunc) {
    this.time = time;
    this.pid = pid;
    this.tid = tid;
    this.tag = tag;
    this.bridgeType = bridgeType;
    this.content = content;
    this.calledFunc = calledFunc;
  }

  static messageByLine(line) {
    /*  TODO make the searching better by using regex.
        Receives a line of a log, for example:
            "08-16 14:41:22.775  2738  2968 I ReactNativeJS: JS->N : RKUIManager.measure([14,15])"
        and returns an object parsed by it. */

    const details = _.filter(line.split(" "), (x) => x != '');

    try {

      const time = moment(details[1], "h:m:s").toDate();
      const pid = details[2];
      const tid = details[3];
      const tag = details[5];
      const bridgeType = details[6];
      const content = details[8];
      const calledFunc = line.split("(")[0].split(" ").pop(); // pop becauge I want to get last of the array

      return new Message(time, pid, tid, tag, bridgeType, content, calledFunc);

    }
    catch (Error) {
      return undefined;
    }
  }

  static messagesByLog(log) {
    const lines = log.split("\n");
    return _.filter(_.map(lines, (line) => Message.messageByLine(line)), (message) => { return message} );
  }

  static dictOfMessagesByTime(messages) {
    var myDict = {};
    messages.forEach((message) => {
      if (_.has(myDict, message.time)) {
        myDict[message.time].push(message);
      }
      else {
        myDict[message.time] = [message];
      }
    });

    return myDict;
  }

  static dictOfMessagesByCalledFunc(messages) {
    const myDict = {};
    messages.forEach((message) => {
      if (_.has(myDict, message.calledFunc)) {
        myDict[message.calledFunc].push(message);
      }
      else {
        myDict[message.calledFunc] = [message]
      }
    });

    return myDict;
  }

  static filterByBridgeType(messages, bridgeType) {
    return _.filter(messages, (message) => message.bridgeType == bridgeType)
  }
  static filterByCalledFunc(messages, calledFunc) {
    return _.filter(messages, (message) => messages.calledFunc == calledFunc);
  }

}

module.exports = Message;
