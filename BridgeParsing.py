from datetime import datetime

NATIVE_TO_JS = "N->JS"
JS_TO_NATIVE = "JS->N"


class Message:

    def __init__(self, time, pid, tid, tag, bridge_type, content, called_func):
        self.time = time
        self.pid = pid
        self.tid = tid
        self.tag = tag
        self.bridge_type = bridge_type
        self.content = content
        self.called_func = called_func

    @staticmethod
    def message_by_line(line):
        """
        TODO make the searching better by using regex.
        Receives a line of a log, for example:
            "08-16 14:41:22.775  2738  2968 I ReactNativeJS: JS->N : RKUIManager.measure([14,15])"
        and returns an object parsed by it.
        """
        details = [x for x in line.split(" ") if x != '']

        try:
            time = datetime.strptime(details[1], '%H:%M:%S.%f')
            pid = details[2]
            tid = details[3]
            tag = details[5]
            bridge_type = details[6]
            content = details[7]
            called_func = line.split("(")[0].split(" ")[-1]

            return Message(time, pid, tid, tag, bridge_type, content, called_func)

        except ValueError:
            return None
        except IndexError:
            return None

    @staticmethod
    def messages_by_log(log):
        """
        Receives a full log
        """
        lines = log.split("\n")
        return [message for message in [Message.message_by_line(line) for line in lines] if message]

    @staticmethod
    def dict_of_messages_by_time(messages):
        my_dict = {}
        for message in messages:
            time = datetime(year=datetime.now().year,
                            month=datetime.now().month,
                            day=datetime.now().day,
                            hour=message.time.hour,
                            minute=message.time.minute,
                            second=message.time.second)

            if time in my_dict:
                my_dict[time].append(message)
            else:
                my_dict[time] = [message]

        return my_dict

    @staticmethod
    def dict_of_messages_by_called_func(messages):
        my_dict = {}
        for message in messages:
            if message.called_func in my_dict:
                my_dict[message.called_func].append(message)
            else:
                my_dict[message.called_func] = [message]
        return my_dict

    @staticmethod
    def get_sorted_times(messages):
        return Message.dict_of_messages_by_time(messages).keys().sort()

    @staticmethod
    def filter_by_bridge_type(messages, bridge_type):
        return [message for message in messages if message.bridge_type == bridge_type]

    @staticmethod
    def filter_by_called_fnc(messages, called_func):
        return [message for message in messages if message.called_func == called_func]



