import uuid
from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
    Integer,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    features: Mapped[list["FeatureCategory"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    releases: Mapped[list["ReleaseVersion"]] = relationship(back_populates="project", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("name", name="uq_project_name"),)


class FeatureCategory(Base):
    __tablename__ = "feature_categories"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid), ForeignKey("projects_id"), ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    project: Mapped["Project"] = relationship(back_populates="features")
    entries: Mapped[list["ChangeEntry"]] = relationship(back_populates="feature", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_feature_project_name"),)

class ReleaseVersion(Base):
    __tablename__ = "release_versions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    version_label: Mapped[str] = mapped_column(String(40), nullable=False)
    title: Mapped[str | None] = mapped_column(String(140))
    summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    project: Mapped["Project"] = relationship(back_populates="releases")
    entries: Mapped[list["ChangeEntry"]] = relationship(back_populates="release", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("project_id", "version_label", name="uq_release_project_version"),)

class ChangeEntry(Base):
    __tablename__ = "change_entries"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    release_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("release_versions.id", ondelete="CASCADE"), nullable=False)
    feature_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("feature_categories.id", ondelete="CASCADE"), nullable=False)

    change_type: Mapped[str] = mapped_column(String(16), nullable=False)  # ADDED/CHANGED/REMOVED
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    details_md: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    release: Mapped["ReleaseVersion"] = relationship(back_populates="entries")
    feature: Mapped["FeatureCategory"] = relationship(back_populates="entries")