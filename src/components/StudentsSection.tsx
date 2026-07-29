import { Search } from "lucide-react";
import { forwardRef, useMemo, useState } from "react";
import {
  alumniItems,
  siteContent,
  studentItems,
  type StudentItem,
} from "../data/siteContent";

type StudentSubsectionProps = {
  heading: string;
  searchLabel: string;
  searchPlaceholder: string;
  noMatchesPrefix: string;
  emptyMessage: string;
  items: StudentItem[];
  sortBy: "startYear" | "endYear";
};

function StudentSubsection({
  heading,
  searchLabel,
  searchPlaceholder,
  noMatchesPrefix,
  emptyMessage,
  items,
  sortBy,
}: StudentSubsectionProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const normalizedQuery = searchQuery.trim().toLocaleLowerCase();

  const filteredItems = useMemo(() => {
    const queryTerms = normalizedQuery.split(/\s+/).filter(Boolean);

    return items
      .filter(({ name, description, startYear, endYear }) => {
        const searchableText =
          `${name} ${description} ${startYear} ${endYear ?? ""}`.toLocaleLowerCase();
        return queryTerms.every((term) => searchableText.includes(term));
      })
      .sort((a, b) => {
        if (sortBy === "startYear") {
          return a.startYear - b.startYear;
        }

        const yearDifference =
          (b.endYear ?? Number.NEGATIVE_INFINITY) -
          (a.endYear ?? Number.NEGATIVE_INFINITY);
        return yearDifference || a.name.localeCompare(b.name);
      });
  }, [items, normalizedQuery, sortBy]);

  return (
    <div className="student-subsection">
      <h2 className="publication-heading students-heading">{heading}</h2>

      <div className="student-controls">
        <label className="student-search">
          <Search size={18} aria-hidden="true" />
          <span className="sr-only">{searchLabel}</span>
          <input
            type="search"
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            placeholder={searchPlaceholder}
          />
        </label>
      </div>

      <div className="students-grid" aria-live="polite">
        {filteredItems.map((student) => {
          const cardContent = (
            <>
              <img
                className="student-picture"
                src={student.picture ?? "default-profile.svg"}
                alt={
                  student.picture
                    ? (student.pictureAlt ?? student.name)
                    : ""
                }
              />
              <h2>{student.name}</h2>
              <span className="student-years">
                {student.startYear}
                {student.endYear ? `–${student.endYear}` : ""}
              </span>
              <p>{student.description}</p>
            </>
          );

          return student.profileUrl ? (
            <a
              className="student-card student-card-link"
              href={student.profileUrl}
              target="_blank"
              rel="noreferrer"
              key={`${student.name}-${student.description}`}
            >
              {cardContent}
            </a>
          ) : (
            <article
              className="student-card"
              key={`${student.name}-${student.description}`}
            >
              {cardContent}
            </article>
          );
        })}

        {filteredItems.length === 0 && (
          <p className="students-empty">
            {normalizedQuery
              ? `${noMatchesPrefix} “${searchQuery.trim()}”.`
              : emptyMessage}
          </p>
        )}
      </div>
    </div>
  );
}

export const StudentsSection = forwardRef<HTMLElement>(
  function StudentsSection(_, ref) {
    const content = siteContent.students;

    return (
      <section id="students" ref={ref} className="students-section">
        <div className="section-kicker">
          <span>{content.sectionNumber}</span>
          <p>{content.sectionTitle}</p>
          <div />
        </div>

        <div className="students-content">
          <StudentSubsection
            {...content.subsections.alumni}
            items={alumniItems}
            sortBy="endYear"
          />
          <StudentSubsection
            {...content.subsections.students}
            items={studentItems}
            sortBy="startYear"
          />
        </div>
      </section>
    );
  },
);
