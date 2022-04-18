export function Rating(props) {
    return (<div>
        <h6>{props.username}</h6>
        <input type="number" onChange={props.onRate} value={props.rating} min="1" max="5"/>
        <input value={props.content} onChange={props.onEdit}/>
        <button onClick={props.onDelete}>Delete</button>
    </div>);
}

