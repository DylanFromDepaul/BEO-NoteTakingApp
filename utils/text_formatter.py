class TextFormatter:
    @staticmethod
    def format_header(text):
        return f"__{text}__"

    @staticmethod
    def format_event(event):
        lines = []
        if event.date:
            lines.append(f"**{event.date} - {event.name}:**")
        else:
            lines.append(f"**{event.name}:**")

        time_str = f"{event.start_time}"
        if event.end_time:
            time_str += f" - {event.end_time}"
        if time_str:
            lines.append(f"Time: {time_str}")

        if event.location:
            lines.append(f"Location: {event.location}")

        if event.equipment:
            lines.append(f"Equipment: {event.equipment}")

        if event.notes:
            lines.append(f"Notes: {event.notes}")

        return "\n".join(lines)

    @staticmethod
    def format_beo(dates):
        formatted_text = ""
        for date in dates:
            formatted_text += f"{date.date_str}\n\n"
            for group in date.get_all_groups():
                formatted_text += f"{group.name}\n"
                for meeting in group.get_all_meetings():
                    formatted_text += f"{meeting.name}\n"
                    if meeting.notes:
                        formatted_text += f"{meeting.notes}\n"
                    if meeting.location:
                        formatted_text += f"Location: {meeting.location}\n"
                    for event in meeting.get_all_events():
                        lines = []
                        time_str = ""
                        if event.name:
                            time_str += f"{event.name}: "
                        time_str += f"{event.start_time} - {event.end_time}"
                        if time_str.strip():
                            lines.append(time_str)
                        if event.equipment:
                            lines.append(f"Equipment: {event.equipment}")
                        formatted_text += "\n".join(lines) + "\n"
                    formatted_text += "\n"
                formatted_text += "\n"
            formatted_text += "\n"
        return formatted_text.strip()
