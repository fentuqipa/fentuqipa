import { Search } from "lucide-react";
import {
  isValidElement,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  alumniItems,
  conferencePublications,
  journalPublications,
  siteContent,
  studentItems,
  underReviewPublications,
  workingPaperPublications,
  type SectionId,
  type TimelinePublication,
} from "../data/siteContent";

type SearchOverlayProps = {
  open: boolean;
  onClose: () => void;
  onSelect: (id: SectionId) => void;
};

type SearchEntry = {
  id: string;
  sectionId: SectionId;
  group: string;
  title: string;
  subtitle: string;
  searchText: string;
  color: string;
  badge?: string;
  overview?: boolean;
};

type SearchableGroup = {
  title: string;
  details: readonly ReactNode[];
};

const sectionColors: Record<SectionId, string> = {
  about: "#00a878",
  research: "#7c4dff",
  teaching: "#ff9f1c",
  services: "#00a8a8",
  awards: "#f05a28",
  students: "#d98200",
};

function normalize(value: string) {
  return value.toLocaleLowerCase().trim();
}

function getSearchableText(value: unknown): string {
  if (typeof value === "string" || typeof value === "number") {
    return String(value);
  }

  if (Array.isArray(value)) {
    return value.map(getSearchableText).join(" ");
  }

  if (isValidElement<{ children?: ReactNode }>(value)) {
    return getSearchableText(value.props.children);
  }

  if (value && typeof value === "object") {
    return Object.values(value).map(getSearchableText).join(" ");
  }

  return "";
}

function createGroupEntries(
  sectionId: SectionId,
  group: string,
  groups: readonly SearchableGroup[],
): SearchEntry[] {
  return groups.map((item, index) => {
    const details = getSearchableText(item.details);

    return {
      id: `${sectionId}-group-${index}`,
      sectionId,
      group,
      title: item.title,
      subtitle: details,
      searchText: `${item.title} ${details}`,
      color: sectionColors[sectionId],
    };
  });
}

function createPublicationEntries(
  label: string,
  badge: string,
  items: TimelinePublication[],
): SearchEntry[] {
  return items.map((publication, index) => {
    const citation = getSearchableText(publication.text);
    const subtitle = publication.year
      ? `${badge} · ${publication.year}`
      : badge;

    return {
      id: `research-${badge.toLocaleLowerCase().replaceAll(" ", "-")}-${index}`,
      sectionId: "research",
      group: label,
      title: citation,
      subtitle,
      searchText: `${citation} ${publication.year} ${badge}`,
      color: sectionColors.research,
      badge,
    };
  });
}

function createSearchEntries(): SearchEntry[] {
  const entries: SearchEntry[] = [
    {
      id: "about-overview",
      sectionId: "about",
      group: "Jump to",
      title: siteContent.about.name,
      subtitle: siteContent.about.status,
      searchText: getSearchableText(siteContent.about),
      color: sectionColors.about,
      overview: true,
    },
    {
      id: "research-overview",
      sectionId: "research",
      group: "Jump to",
      title: "Research",
      subtitle:
        "Journal publications, conference publications, papers under review, and working papers",
      searchText: "research publications journals conferences under review working papers",
      color: sectionColors.research,
      overview: true,
    },
    {
      id: "teaching-overview",
      sectionId: "teaching",
      group: "Jump to",
      title: siteContent.teaching.sectionTitle,
      subtitle: siteContent.teaching.groups.map(({ title }) => title).join(", "),
      searchText: getSearchableText(siteContent.teaching),
      color: sectionColors.teaching,
      overview: true,
    },
    {
      id: "services-overview",
      sectionId: "services",
      group: "Jump to",
      title: siteContent.services.sectionTitle,
      subtitle: siteContent.services.groups.map(({ title }) => title).join(", "),
      searchText: getSearchableText(siteContent.services),
      color: sectionColors.services,
      overview: true,
    },
    {
      id: "awards-overview",
      sectionId: "awards",
      group: "Jump to",
      title: siteContent.awards.sectionTitle,
      subtitle: siteContent.awards.groups.map(({ title }) => title).join(", "),
      searchText: getSearchableText(siteContent.awards),
      color: sectionColors.awards,
      overview: true,
    },
    {
      id: "students-overview",
      sectionId: "students",
      group: "Jump to",
      title: siteContent.students.sectionTitle,
      subtitle: "Current students and alumni",
      searchText: getSearchableText(siteContent.students),
      color: sectionColors.students,
      overview: true,
    },
  ];

  entries.push(
    ...createGroupEntries("about", "About", siteContent.about.groups),
    ...createGroupEntries(
      "teaching",
      siteContent.teaching.sectionTitle,
      siteContent.teaching.groups,
    ),
    ...createGroupEntries(
      "services",
      siteContent.services.sectionTitle,
      siteContent.services.groups,
    ),
    ...createGroupEntries(
      "awards",
      siteContent.awards.sectionTitle,
      siteContent.awards.groups,
    ),
    ...alumniItems.map((alumnus, index) => ({
      id: `alumnus-${index}`,
      sectionId: "students" as const,
      group: siteContent.students.subsections.alumni.heading,
      title: alumnus.name,
      subtitle: alumnus.description.replaceAll("\n", " · "),
      searchText: getSearchableText(alumnus),
      color: sectionColors.students,
      badge: siteContent.students.subsections.alumni.heading,
    })),
    ...studentItems.map((student, index) => ({
      id: `student-${index}`,
      sectionId: "students" as const,
      group: siteContent.students.subsections.students.heading,
      title: student.name,
      subtitle: student.description.replaceAll("\n", " · "),
      searchText: getSearchableText(student),
      color: sectionColors.students,
      badge: siteContent.students.subsections.students.heading,
    })),
    ...createPublicationEntries(
      "Journal Publications",
      "Journal",
      journalPublications,
    ),
    ...createPublicationEntries(
      "Conference Publications",
      "Conference",
      conferencePublications,
    ),
    ...createPublicationEntries(
      "Under Review",
      "Under Review",
      underReviewPublications,
    ),
    ...createPublicationEntries(
      "Working Papers",
      "Working Paper",
      workingPaperPublications,
    ),
  );

  return entries;
}

const generatedSearchEntries = createSearchEntries();

export function SearchOverlay({
  open,
  onClose,
  onSelect,
}: SearchOverlayProps) {
  const [query, setQuery] = useState("");

  const results = useMemo(() => {
    const queryTerms = normalize(query).split(/\s+/).filter(Boolean);

    if (queryTerms.length === 0) {
      return generatedSearchEntries.filter(({ overview }) => overview);
    }

    return generatedSearchEntries.filter((item) => {
      const haystack = normalize(
        `${item.title} ${item.subtitle} ${item.group} ${item.searchText}`,
      );

      return queryTerms.every((word) => haystack.includes(word));
    });
  }, [query]);

  const groupedResults = useMemo(() => {
    return results.reduce<Record<string, SearchEntry[]>>((acc, item) => {
      acc[item.group] ??= [];
      acc[item.group].push(item);
      return acc;
    }, {});
  }, [results]);

  if (!open) return null;

  return (
    <div className="search-backdrop" onMouseDown={onClose}>
      <div
        className="search-panel"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="search-input-row">
          <Search size={18} />
          <input
            autoFocus
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder={siteContent.search.placeholder}
          />
          <button onClick={onClose}>{siteContent.search.closeLabel}</button>
        </div>

        <div className="search-results-list">
          {Object.entries(groupedResults).map(([group, items]) => (
            <div className="search-group" key={group}>
              <p className="search-group-title">{group}</p>

              {items.map((item) => (
                <button
                  key={item.id}
                  className="search-result"
                  onClick={() => onSelect(item.sectionId)}
                >
                  <span
                    className="result-dot"
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="result-text">
                    <span>
                      {item.title}
                      {item.badge && <em>{item.badge}</em>}
                    </span>
                    <small>{item.subtitle}</small>
                  </span>
                  <kbd>{siteContent.search.resultKey}</kbd>
                </button>
              ))}
            </div>
          ))}

          {results.length === 0 && (
            <div className="empty-search">
              {siteContent.search.emptyMessage}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
