# social-media-api
## Backend clone  of social media app by using FastAPI


@router.get("/{id}", response_model=schemas.PostWithVotesOut)
async def get_post_with_votes(id: int, db: Session = Depends(get_db)):
    # Fetch the post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist!"
        )

    # Lazily load votes and voters
    votes_count = len(post.votes)
    voters = [
        {"id": vote.user.id, "name": vote.user.name} for vote in post.votes if vote.user
    ]

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "datetime_created": post.datetime_created,
        "owner": {"id": post.owner.id, "name": post.owner.name},
        "votes_count": votes_count,
        "voters": voters,
    }

    
class PostWithVotesOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    datetime_created: datetime
    owner: PostOwner
    votes_count: int
    voters: List[PostVoter]

    class Config:
        orm_mode = True
 