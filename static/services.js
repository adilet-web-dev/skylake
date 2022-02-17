const EVENTS = {
	"UPDATE_ONLINE_USERS_NUMBER": "update_online_users_number",
	"COMMENT": "comment",
	"VOTE": "vote",
    "UPDATE_VOTES": "update_votes"
}


class WebsocketService extends WebSocket {
    constructor(url) {
        super(url);
    }

    voteCandidate(candidate){
        this.send(JSON.stringify({
            "event": "vote",
            "candidate": candidate
        }))
    }

    comment(comment){
        this.send(JSON.stringify({
            "event": "comment",
            "comment": comment
        }))
    }

}
